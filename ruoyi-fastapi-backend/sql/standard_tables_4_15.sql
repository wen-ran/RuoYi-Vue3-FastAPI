-- ----------------------------
-- 1、标准基础信息表
-- ----------------------------
drop table if exists standard_info;
create table standard_info (
  id                    bigint(20)      default null               comment '主键ID',
  standard_no           varchar(100)    default null               comment '标准号',
  name_zh               varchar(500)    default null               comment '中文名称',
  name_en               varchar(500)    default null               comment '英文名称',
  ics                   varchar(100)    default null               comment 'ICS分类号',
  ccs                   varchar(100)    default null               comment 'CCS分类号',
  cn_standard_class_no  varchar(100)    default null               comment '中标分类号',
  technical_committee   varchar(255)    default null               comment '所属技术委员会',
  release_date          date            default null               comment '发布时间',
  effective_date        date            default null               comment '实施时间',
  issuing_organization  varchar(255)    default null               comment '发布单位',
  status                varchar(50)     default null               comment '状态',
  file_path             varchar(500)    default null               comment '文件地址',
  created_at            datetime        default null               comment '创建时间',
  created_by            varchar(64)     default null               comment '创建人',
  updated_at            datetime        default null               comment '更新时间',
  updated_by            varchar(64)     default null               comment '更新人',
  is_deleted            int(1)          default null               comment '是否删除',
  remark                varchar(500)    default null               comment '备注'
) engine=innodb comment = '标准基础信息表';


-- ----------------------------
-- 2、标准正文内容表
-- ----------------------------
drop table if exists standard_content;
create table standard_content (
  id                    bigint(20)      default null               comment '主键ID',
  standard_no           varchar(100)    default null               comment '标准号',
  parent_node_id        bigint(20)      default null               comment '父节点ID',
  sibling_order_no      int(4)          default null               comment '同级内排序号',
  content_level         int(4)          default null               comment '内容层级',
  source_page_no        int(4)          default null               comment '所在文件页面',
  clause_no             varchar(100)    default null               comment '条款编号',
  content_type          varchar(100)    default null               comment '内容类型（关联文档类型字典）',
  content_text_with_no  text                                       comment '内容（包含编号）；如出现上标或下标直接存C₂；只有公式占空行，图表存“图x/表x”',
  is_mandatory          int(1)          default null               comment '是否强制',
  created_at            datetime        default null               comment '创建时间',
  created_by            varchar(64)     default null               comment '创建人',
  updated_at            datetime        default null               comment '更新时间',
  updated_by            varchar(64)     default null               comment '更新人',
  is_deleted            int(1)          default null               comment '是否删除',
  remark                varchar(500)    default null               comment '备注'
) engine=innodb comment = '标准正文内容表';


-- ----------------------------
-- 3、文档类型表
-- ----------------------------
drop table if exists document_type;
create table document_type (
  type_name             varchar(100)    default null               comment '类型',
  sort_no               int(4)          default null               comment '序号',
  created_at            datetime        default null               comment '创建时间',
  created_by            varchar(64)     default null               comment '创建人',
  updated_at            datetime        default null               comment '更新时间',
  updated_by            varchar(64)     default null               comment '更新人',
  is_deleted            int(1)          default null               comment '是否删除',
  remark                varchar(500)    default null               comment '备注'
) engine=innodb comment = '文档类型表';


-- ----------------------------
-- 初始化-文档类型表数据
-- ----------------------------
insert into document_type values('图片',       1, null, null, null, null, null, null);
insert into document_type values('表格',       2, null, null, null, null, null, null);
insert into document_type values('公式',       3, null, null, null, null, null, null);
insert into document_type values('标题',       4, null, null, null, null, null, null);
insert into document_type values('有编号内容', 5, null, null, null, null, null, null);
insert into document_type values('无编号内容', 6, null, null, null, null, null, null);
