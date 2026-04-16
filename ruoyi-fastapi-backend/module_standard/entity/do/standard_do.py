from sqlalchemy import BigInteger, Column, Date, DateTime, Integer, String, Text

from config.database import Base


class StandardInfo(Base):
    """
    标准基础信息表
    """

    __tablename__ = 'standard_info'
    __table_args__ = {'comment': '标准基础信息'}

    id = Column(BigInteger, nullable=True, comment='主键ID')
    standard_no = Column(String(100), nullable=True, comment='标准号')
    name_zh = Column(String(500), nullable=True, comment='中文名称')
    name_en = Column(String(500), nullable=True, comment='英文名称')
    ics = Column(String(100), nullable=True, comment='ICS分类号')
    ccs = Column(String(100), nullable=True, comment='CCS分类号')
    cn_standard_class_no = Column(String(100), nullable=True, comment='中标分类号')
    technical_committee = Column(String(255), nullable=True, comment='所属技术委员会')
    release_date = Column(Date, nullable=True, comment='发布时间')
    effective_date = Column(Date, nullable=True, comment='实施时间')
    issuing_organization = Column(String(255), nullable=True, comment='发布单位')
    status = Column(String(50), nullable=True, comment='状态')
    file_path = Column(String(500), nullable=True, comment='文件地址')
    created_at = Column(DateTime, nullable=True, comment='创建时间')
    created_by = Column(String(64), nullable=True, comment='创建人')
    updated_at = Column(DateTime, nullable=True, comment='更新时间')
    updated_by = Column(String(64), nullable=True, comment='更新人')
    is_deleted = Column(Integer, nullable=True, comment='是否删除')
    remark = Column(String(500), nullable=True, comment='备注')

    __mapper_args__ = {'primary_key': [id, standard_no]}


class StandardContent(Base):
    """
    标准正文内容表
    """

    __tablename__ = 'standard_content'
    __table_args__ = {'comment': '标准正文内容'}

    id = Column(BigInteger, nullable=True, comment='主键ID')
    standard_no = Column(String(100), nullable=True, comment='标准号')
    parent_node_id = Column(BigInteger, nullable=True, comment='父节点ID')
    sibling_order_no = Column(Integer, nullable=True, comment='同级内排序号')
    content_level = Column(Integer, nullable=True, comment='内容层级')
    source_page_no = Column(Integer, nullable=True, comment='所在文件页面')
    clause_no = Column(String(100), nullable=True, comment='条款编号')
    content_type = Column(String(100), nullable=True, comment='内容类型（关联文档类型字典）')
    content_text_with_no = Column(
        Text,
        nullable=True,
        comment='内容（包含编号）；如出现上标或下标直接存C₂；只有公式占空行，图表存“图x/表x”',
    )
    is_mandatory = Column(Integer, nullable=True, comment='是否强制')
    created_at = Column(DateTime, nullable=True, comment='创建时间')
    created_by = Column(String(64), nullable=True, comment='创建人')
    updated_at = Column(DateTime, nullable=True, comment='更新时间')
    updated_by = Column(String(64), nullable=True, comment='更新人')
    is_deleted = Column(Integer, nullable=True, comment='是否删除')
    remark = Column(String(500), nullable=True, comment='备注')

    __mapper_args__ = {'primary_key': [id, standard_no]}


class DocumentType(Base):
    """
    文档类型表
    """

    __tablename__ = 'document_type'
    __table_args__ = {'comment': '文档类型'}

    type_name = Column(String(100), nullable=True, comment='类型')
    sort_no = Column(Integer, nullable=True, comment='序号')
    created_at = Column(DateTime, nullable=True, comment='创建时间')
    created_by = Column(String(64), nullable=True, comment='创建人')
    updated_at = Column(DateTime, nullable=True, comment='更新时间')
    updated_by = Column(String(64), nullable=True, comment='更新人')
    is_deleted = Column(Integer, nullable=True, comment='是否删除')
    remark = Column(String(500), nullable=True, comment='备注')

    __mapper_args__ = {'primary_key': [type_name, sort_no]}
