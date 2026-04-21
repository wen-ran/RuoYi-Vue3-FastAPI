from datetime import datetime
from typing import Any

from sqlalchemy import ColumnElement, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import PageModel
from module_standard.entity.do.standard_do import StdStandardInfo
from module_standard.entity.vo.standard_vo import StandardInfoPageQueryModel
from utils.page_util import PageUtil


class StandardInfoDao:
    """
    标准基础信息数据操作层
    """

    @classmethod
    def _not_blank(cls, column: ColumnElement) -> tuple[ColumnElement, ColumnElement]:
        """
        生成字段非空白的查询条件

        :param column: 数据库字段
        :return: 非空且去除空格后不为空字符串的查询条件
        """
        return column.is_not(None), func.trim(column) != ''

    @classmethod
    def _blank(cls, column: ColumnElement) -> ColumnElement:
        """
        生成字段为空白的查询条件

        :param column: 数据库字段
        :return: 为空或去除空格后为空字符串的查询条件
        """
        return or_(column.is_(None), func.trim(column) == '')

    @classmethod
    async def get_pending_upload_list(
        cls,
        db: AsyncSession,
        query_object: StandardInfoPageQueryModel,
        is_page: bool = False,
    ) -> PageModel | list[dict[str, Any]]:
        """
        根据查询参数获取待上传标准列表

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 待上传标准列表信息对象
        """
        query = (
            select(StdStandardInfo)
            .where(
                *cls._not_blank(StdStandardInfo.standard_no),
                *cls._not_blank(StdStandardInfo.name_zh),
                cls._blank(StdStandardInfo.file_path),
                or_(StdStandardInfo.is_deleted.is_(None), StdStandardInfo.is_deleted == 0),
                StdStandardInfo.standard_no.like(f'%{query_object.standard_no}%')
                if query_object.standard_no
                else True,
                StdStandardInfo.name_zh.like(f'%{query_object.name_zh}%') if query_object.name_zh else True,
            )
            .order_by(StdStandardInfo.standard_no, StdStandardInfo.id)
        )

        return await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

    @classmethod
    async def get_standard_for_upload(
        cls,
        db: AsyncSession,
        standard_id: int | None,
        standard_no: str | None,
    ) -> StdStandardInfo | None:
        """
        根据标准ID或标准号获取待上传标准信息

        :param db: orm对象
        :param standard_id: 标准ID
        :param standard_no: 标准号
        :return: 标准基础信息对象
        """
        where_clause = StdStandardInfo.id == standard_id if standard_id is not None else StdStandardInfo.standard_no == standard_no
        return (await db.execute(select(StdStandardInfo).where(where_clause))).scalars().first()

    @classmethod
    async def update_file_path(
        cls,
        db: AsyncSession,
        standard_info: StdStandardInfo,
        file_path: str,
        updated_at: datetime,
        updated_by: str | None,
    ) -> None:
        """
        更新标准文件地址

        :param db: orm对象
        :param standard_info: 标准基础信息对象
        :param file_path: 文件映射地址
        :param updated_at: 更新时间
        :param updated_by: 更新人
        :return:
        """
        where_conditions = []
        if standard_info.id is not None:
            where_conditions.append(StdStandardInfo.id == standard_info.id)
        if standard_info.standard_no:
            where_conditions.append(StdStandardInfo.standard_no == standard_info.standard_no)

        await db.execute(
            update(StdStandardInfo)
            .where(*where_conditions)
            .values(file_path=file_path, updated_at=updated_at, updated_by=updated_by)
        )
