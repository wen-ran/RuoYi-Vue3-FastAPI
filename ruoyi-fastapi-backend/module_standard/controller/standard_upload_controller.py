from typing import Annotated

from fastapi import File, Form, Query, Request, Response, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from common.aspect.db_seesion import DBSessionDependency
from common.aspect.interface_auth import UserInterfaceAuthDependency
from common.aspect.pre_auth import CurrentUserDependency, PreAuthDependency
from common.router import APIRouterPro
from common.vo import DynamicResponseModel, PageResponseModel
from module_admin.entity.vo.common_vo import UploadResponseModel
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_standard.entity.vo.standard_vo import StandardInfoModel, StandardInfoPageQueryModel
from module_standard.service.standard_upload_service import StandardUploadService
from utils.log_util import logger
from utils.response_util import ResponseUtil

standard_upload_controller = APIRouterPro(
    prefix='/standard/upload',
    order_num=19,
    tags=['标准管理-标准上传'],
    dependencies=[PreAuthDependency()],
)


@standard_upload_controller.get(
    '/list',
    summary='获取待上传标准列表',
    description='查询有标准号、中文名且文件地址为空的标准信息',
    response_model=PageResponseModel[StandardInfoModel],
    dependencies=[UserInterfaceAuthDependency('standard:upload:list')],
)
async def get_pending_standard_upload_list(
    request: Request,
    standard_query: Annotated[StandardInfoPageQueryModel, Query()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    # 获取分页数据
    result = await StandardUploadService.get_pending_upload_list_services(query_db, standard_query, is_page=True)
    logger.info('获取待上传标准列表成功')

    return ResponseUtil.success(model_content=result)


@standard_upload_controller.post(
    '',
    summary='上传标准文件',
    description='保存标准文件到本地并回填标准文件地址',
    response_model=DynamicResponseModel[UploadResponseModel],
    dependencies=[UserInterfaceAuthDependency('standard:upload:file')],
)
async def upload_standard_file(
    request: Request,
    file: Annotated[UploadFile, File(...)],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
    standard_id: Annotated[int | None, Form(alias='id')] = None,
    standard_no: Annotated[str | None, Form(alias='standardNo')] = None,
) -> Response:
    # 上传文件并回填标准文件地址
    upload_result = await StandardUploadService.upload_standard_file_services(
        request=request,
        query_db=query_db,
        file=file,
        standard_id=standard_id,
        standard_no=standard_no,
        updated_by=current_user.user.user_name,
    )
    logger.info(upload_result.message)

    return ResponseUtil.success(msg=upload_result.message, model_content=upload_result.result)
