from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class StandardInfoModel(BaseModel):
    """
    标准基础信息表对应pydantic模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: int | None = Field(default=None, description='主键ID')
    standard_no: str | None = Field(default=None, description='标准号')
    name_zh: str | None = Field(default=None, description='中文名称')
    name_en: str | None = Field(default=None, description='英文名称')
    ics: str | None = Field(default=None, description='ICS分类号')
    ccs: str | None = Field(default=None, description='CCS分类号')
    cn_standard_class_no: str | None = Field(default=None, description='中标分类号')
    technical_committee: str | None = Field(default=None, description='所属技术委员会')
    release_date: date | None = Field(default=None, description='发布时间')
    effective_date: date | None = Field(default=None, description='实施时间')
    issuing_organization: str | None = Field(default=None, description='发布单位')
    status: str | None = Field(default=None, description='状态')
    file_path: str | None = Field(default=None, description='文件地址')
    created_at: datetime | None = Field(default=None, description='创建时间')
    created_by: str | None = Field(default=None, description='创建人')
    updated_at: datetime | None = Field(default=None, description='更新时间')
    updated_by: str | None = Field(default=None, description='更新人')
    is_deleted: int | None = Field(default=None, description='是否删除')
    remark: str | None = Field(default=None, description='备注')


class StandardInfoPageQueryModel(StandardInfoModel):
    """
    标准基础信息分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class StandardContentModel(BaseModel):
    """
    标准正文内容表对应pydantic模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: int | None = Field(default=None, description='主键ID')
    standard_no: str | None = Field(default=None, description='标准号')
    parent_node_id: int | None = Field(default=None, description='父节点ID')
    sibling_order_no: int | None = Field(default=None, description='同级内排序号')
    content_level: int | None = Field(default=None, description='内容层级')
    source_page_no: int | None = Field(default=None, description='所在文件页面')
    clause_no: str | None = Field(default=None, description='条款编号')
    content_type: str | None = Field(default=None, description='内容类型（关联文档类型字典）')
    content_text_with_no: str | None = Field(
        default=None,
        description='内容（包含编号）；如出现上标或下标直接存C₂；只有公式占空行，图表存“图x/表x”',
    )
    is_mandatory: int | None = Field(default=None, description='是否强制')
    created_at: datetime | None = Field(default=None, description='创建时间')
    created_by: str | None = Field(default=None, description='创建人')
    updated_at: datetime | None = Field(default=None, description='更新时间')
    updated_by: str | None = Field(default=None, description='更新人')
    is_deleted: int | None = Field(default=None, description='是否删除')
    remark: str | None = Field(default=None, description='备注')


class StandardContentPageQueryModel(StandardContentModel):
    """
    标准正文内容分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class StandardContentQueryModel(BaseModel):
    """
    标准正文内容查询结果模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: int | None = Field(default=None, description='主键ID')
    standard_no: str | None = Field(default=None, description='标准号')
    name_zh: str | None = Field(default=None, description='中文名称')
    file_path: str | None = Field(default=None, description='文件地址')
    source_page_no: int | None = Field(default=None, description='所在文件页面')
    clause_no: str | None = Field(default=None, description='条款编号')
    content_type: str | None = Field(default=None, description='内容类型')
    content_text_with_no: str | None = Field(default=None, description='内容（包含编号）')


class StandardContentQueryPageQueryModel(BaseModel):
    """
    标准正文内容查询分页参数模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')
    standard_no: str | None = Field(default=None, description='标准号')
    name_zh: str | None = Field(default=None, description='中文名称')
    content_text_with_no: str | None = Field(default=None, description='内容（包含编号）')


class DocumentTypeModel(BaseModel):
    """
    文档类型表对应pydantic模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    type_name: str | None = Field(default=None, description='类型')
    sort_no: int | None = Field(default=None, description='序号')
    created_at: datetime | None = Field(default=None, description='创建时间')
    created_by: str | None = Field(default=None, description='创建人')
    updated_at: datetime | None = Field(default=None, description='更新时间')
    updated_by: str | None = Field(default=None, description='更新人')
    is_deleted: int | None = Field(default=None, description='是否删除')
    remark: str | None = Field(default=None, description='备注')


class DocumentTypePageQueryModel(DocumentTypeModel):
    """
    文档类型分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')
