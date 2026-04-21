import os
import re
from datetime import datetime
from typing import Any

import aiofiles
from anyio import Path as AsyncPath
from fastapi import Request, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import CrudResponseModel, PageModel
from config.env import UploadConfig
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import UploadResponseModel
from module_standard.dao.standard_info_dao import StandardInfoDao
from module_standard.entity.vo.standard_vo import StandardInfoPageQueryModel
from utils.upload_util import UploadUtil


class StandardUploadService:
    """
    标准文件上传服务层
    """

    @classmethod
    async def get_pending_upload_list_services(
        cls,
        query_db: AsyncSession,
        query_object: StandardInfoPageQueryModel,
        is_page: bool = False,
    ) -> PageModel | list[dict[str, Any]]:
        """
        获取待上传标准列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 待上传标准列表信息对象
        """
        return await StandardInfoDao.get_pending_upload_list(query_db, query_object, is_page)

    @classmethod
    def _safe_filename_part(cls, value: str | None, default: str) -> str:
        """
        生成适合用于本地文件名的片段

        :param value: 原始字段值
        :param default: 默认文件名片段
        :return: 清理后的文件名片段
        """
        safe_value = (value or '').strip()
        safe_value = re.sub(r'[\\/:*?"<>|\s]+', '_', safe_value)
        safe_value = re.sub(r'_+', '_', safe_value).strip('._')
        return (safe_value or default)[:80]

    @classmethod
    def _validate_file(cls, file: UploadFile) -> tuple[str, str]:
        """
        校验上传文件名称和扩展名

        :param file: 上传文件对象
        :return: 原始文件名和文件扩展名
        """
        original_filename = os.path.basename(file.filename or '')
        if not original_filename or '.' not in original_filename:
            raise ServiceException(message='文件名称不合法')

        file_extension = original_filename.rsplit('.', 1)[-1].lower()
        if file_extension not in UploadConfig.DEFAULT_ALLOWED_EXTENSION:
            raise ServiceException(message='文件类型不合法')

        return original_filename, file_extension

    @classmethod
    async def upload_standard_file_services(
        cls,
        request: Request,
        query_db: AsyncSession,
        file: UploadFile,
        standard_id: int | None,
        standard_no: str | None,
        updated_by: str | None,
    ) -> CrudResponseModel:
        """
        上传标准文件并回填文件地址service

        :param request: Request对象
        :param query_db: orm对象
        :param file: 上传文件对象
        :param standard_id: 标准ID
        :param standard_no: 标准号
        :param updated_by: 更新人
        :return: 上传结果
        """
        if standard_id is None and not standard_no:
            raise ServiceException(message='标准标识不能为空')

        standard_info = await StandardInfoDao.get_standard_for_upload(query_db, standard_id, standard_no)
        if not standard_info:
            raise ServiceException(message='标准信息不存在')
        if not standard_info.standard_no or not standard_info.name_zh:
            raise ServiceException(message='标准号和中文名不能为空')
        if standard_info.file_path and standard_info.file_path.strip():
            raise ServiceException(message='该标准已存在文件地址')

        original_filename, file_extension = cls._validate_file(file)
        now = datetime.now()
        relative_path = f'standard/{now.strftime("%Y")}/{now.strftime("%m")}/{now.strftime("%d")}'
        dir_path = os.path.join(UploadConfig.UPLOAD_PATH, relative_path)
        os.makedirs(dir_path, exist_ok=True)

        standard_part = cls._safe_filename_part(standard_info.standard_no, 'standard')
        name_part = cls._safe_filename_part(standard_info.name_zh, 'file')
        filename = (
            f'{standard_part}_{name_part}_{now.strftime("%Y%m%d%H%M%S")}'
            f'{UploadConfig.UPLOAD_MACHINE}{UploadUtil.generate_random_number()}.{file_extension}'
        )
        local_filepath = os.path.join(dir_path, filename)
        mapped_filepath = f'{UploadConfig.UPLOAD_PREFIX}/{relative_path}/{filename}'.replace('//', '/')

        try:
            async with aiofiles.open(local_filepath, 'wb') as f:
                while True:
                    chunk = await file.read(1024 * 1024 * 10)
                    if not chunk:
                        break
                    await f.write(chunk)

            await StandardInfoDao.update_file_path(
                query_db,
                standard_info=standard_info,
                file_path=mapped_filepath,
                updated_at=now,
                updated_by=updated_by,
            )
            await query_db.commit()
        except Exception as e:
            await query_db.rollback()
            saved_file = AsyncPath(local_filepath)
            if await saved_file.exists():
                await saved_file.unlink()
            raise e

        return CrudResponseModel(
            is_success=True,
            result=UploadResponseModel(
                fileName=mapped_filepath,
                newFileName=filename,
                originalFilename=original_filename,
                url=f'{request.base_url}{UploadConfig.UPLOAD_PREFIX[1:]}/{relative_path}/{filename}',
            ),
            message='上传成功',
        )
