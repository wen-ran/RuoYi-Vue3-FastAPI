from typing import Any

from sqlalchemy import ColumnElement, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import PageModel
from module_standard.entity.do.standard_do import StdStandardContent, StdStandardInfo
from module_standard.entity.vo.standard_vo import StandardContentQueryPageQueryModel, StandardInfoPageQueryModel
from utils.page_util import PageUtil


class StandardQueryDao:
    """
    标准查询模块数据库操作层
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
    def _not_deleted(cls, column: ColumnElement) -> ColumnElement:
        """
        生成未删除数据的查询条件

        :param column: 是否删除字段
        :return: 未删除或未设置删除标识的查询条件
        """
        return or_(column.is_(None), column == 0)

    @classmethod
    async def get_standard_list(
        cls,
        db: AsyncSession,
        query_object: StandardInfoPageQueryModel,
        is_page: bool = False,
    ) -> PageModel | list[dict[str, Any]]:
        """
        根据查询参数获取可打开的标准列表

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 标准列表信息对象
        """
        query = (
            select(StdStandardInfo)
            .where(
                cls._not_deleted(StdStandardInfo.is_deleted),
                *cls._not_blank(StdStandardInfo.standard_no),
                *cls._not_blank(StdStandardInfo.name_zh),
                *cls._not_blank(StdStandardInfo.file_path),
                StdStandardInfo.standard_no.like(f'%{query_object.standard_no}%')
                if query_object.standard_no
                else True,
                StdStandardInfo.name_zh.like(f'%{query_object.name_zh}%') if query_object.name_zh else True,
            )
            .order_by(StdStandardInfo.standard_no, StdStandardInfo.id)
        )

        return await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

    @classmethod
    async def get_content_list(
        cls,
        db: AsyncSession,
        query_object: StandardContentQueryPageQueryModel,
        is_page: bool = False,
    ) -> PageModel | list[dict[str, Any]]:
        """
        根据正文内容获取可定位到来源页的标准正文列表

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 标准正文列表信息对象
        """
        query = (
            select(
                StdStandardContent.id.label('id'),
                StdStandardContent.standard_no.label('standard_no'),
                StdStandardInfo.name_zh.label('name_zh'),
                StdStandardInfo.file_path.label('file_path'),
                StdStandardContent.source_page_no.label('source_page_no'),
                StdStandardContent.clause_no.label('clause_no'),
                StdStandardContent.content_type.label('content_type'),
                StdStandardContent.content_text_with_no.label('content_text_with_no'),
            )
            .join(StdStandardInfo, StdStandardInfo.standard_no == StdStandardContent.standard_no)
            .where(
                cls._not_deleted(StdStandardInfo.is_deleted),
                cls._not_deleted(StdStandardContent.is_deleted),
                *cls._not_blank(StdStandardInfo.file_path),
                *cls._not_blank(StdStandardContent.content_text_with_no),
                StdStandardContent.standard_no.like(f'%{query_object.standard_no}%')
                if query_object.standard_no
                else True,
                StdStandardInfo.name_zh.like(f'%{query_object.name_zh}%') if query_object.name_zh else True,
                StdStandardContent.content_text_with_no.like(f'%{query_object.content_text_with_no}%')
                if query_object.content_text_with_no
                else True,
            )
            .order_by(
                StdStandardContent.standard_no,
                StdStandardContent.source_page_no,
                StdStandardContent.sibling_order_no,
                StdStandardContent.id,
            )
        )

        return await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)
