from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import PageModel
from module_standard.dao.standard_query_dao import StandardQueryDao
from module_standard.entity.vo.standard_vo import StandardContentQueryPageQueryModel, StandardInfoPageQueryModel


class StandardQueryService:
    """
    标准查询模块服务层
    """

    @classmethod
    async def get_standard_list_services(
        cls,
        query_db: AsyncSession,
        query_object: StandardInfoPageQueryModel,
        is_page: bool = False,
    ) -> PageModel | list[dict[str, Any]]:
        """
        获取可打开的标准列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 标准列表信息对象
        """
        return await StandardQueryDao.get_standard_list(query_db, query_object, is_page)

    @classmethod
    async def get_content_list_services(
        cls,
        query_db: AsyncSession,
        query_object: StandardContentQueryPageQueryModel,
        is_page: bool = False,
    ) -> PageModel | list[dict[str, Any]]:
        """
        获取标准正文内容列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 标准正文内容列表信息对象
        """
        return await StandardQueryDao.get_content_list(query_db, query_object, is_page)
