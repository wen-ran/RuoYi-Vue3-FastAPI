from typing import Annotated

from fastapi import Query, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from common.aspect.db_seesion import DBSessionDependency
from common.aspect.interface_auth import UserInterfaceAuthDependency
from common.aspect.pre_auth import PreAuthDependency
from common.router import APIRouterPro
from common.vo import PageResponseModel
from module_standard.entity.vo.standard_vo import (
    StandardContentQueryModel,
    StandardContentQueryPageQueryModel,
    StandardInfoModel,
    StandardInfoPageQueryModel,
)
from module_standard.service.standard_query_service import StandardQueryService
from utils.log_util import logger
from utils.response_util import ResponseUtil

standard_query_controller = APIRouterPro(
    prefix='/standard/query',
    order_num=20,
    tags=['标准管理-标准查询'],
    dependencies=[PreAuthDependency()],
)


@standard_query_controller.get(
    '/list',
    summary='获取标准查询列表接口',
    description='用于按标准号、标准名查询可打开的标准文件',
    response_model=PageResponseModel[StandardInfoModel],
    dependencies=[UserInterfaceAuthDependency('standard:query:list')],
)
async def get_standard_query_list(
    request: Request,
    standard_query: Annotated[StandardInfoPageQueryModel, Query()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    # 获取标准文件分页数据
    result = await StandardQueryService.get_standard_list_services(query_db, standard_query, is_page=True)
    logger.info('获取标准查询列表成功')

    return ResponseUtil.success(model_content=result)


@standard_query_controller.get(
    '/content/list',
    summary='获取标准正文查询列表接口',
    description='用于按标准正文内容查询可定位到来源页的标准内容',
    response_model=PageResponseModel[StandardContentQueryModel],
    dependencies=[UserInterfaceAuthDependency('standard:query:content')],
)
async def get_standard_content_query_list(
    request: Request,
    content_query: Annotated[StandardContentQueryPageQueryModel, Query()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    # 获取标准正文分页数据
    result = await StandardQueryService.get_content_list_services(query_db, content_query, is_page=True)
    logger.info('获取标准正文查询列表成功')

    return ResponseUtil.success(model_content=result)
