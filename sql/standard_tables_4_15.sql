-- 数据库设计_4.15.xlsx：标准基础信息、标准正文内容、文档类型
-- 可直接导入 MySQL；按需求保持三张表字段均可为 NULL。

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

CREATE TABLE IF NOT EXISTS `standard_info` (
  `id` BIGINT NULL DEFAULT NULL COMMENT '主键ID',
  `standard_no` VARCHAR(100) NULL DEFAULT NULL COMMENT '标准号',
  `name_zh` VARCHAR(500) NULL DEFAULT NULL COMMENT '中文名称',
  `name_en` VARCHAR(500) NULL DEFAULT NULL COMMENT '英文名称',
  `ics` VARCHAR(100) NULL DEFAULT NULL COMMENT 'ICS分类号',
  `ccs` VARCHAR(100) NULL DEFAULT NULL COMMENT 'CCS分类号',
  `cn_standard_class_no` VARCHAR(100) NULL DEFAULT NULL COMMENT '中标分类号',
  `technical_committee` VARCHAR(255) NULL DEFAULT NULL COMMENT '所属技术委员会',
  `release_date` DATE NULL DEFAULT NULL COMMENT '发布时间',
  `effective_date` DATE NULL DEFAULT NULL COMMENT '实施时间',
  `issuing_organization` VARCHAR(255) NULL DEFAULT NULL COMMENT '发布单位',
  `status` VARCHAR(50) NULL DEFAULT NULL COMMENT '状态',
  `file_path` VARCHAR(500) NULL DEFAULT NULL COMMENT '文件地址',
  `created_at` DATETIME NULL DEFAULT NULL COMMENT '创建时间',
  `created_by` VARCHAR(64) NULL DEFAULT NULL COMMENT '创建人',
  `updated_at` DATETIME NULL DEFAULT NULL COMMENT '更新时间',
  `updated_by` VARCHAR(64) NULL DEFAULT NULL COMMENT '更新人',
  `is_deleted` INT NULL DEFAULT NULL COMMENT '是否删除',
  `remark` VARCHAR(500) NULL DEFAULT NULL COMMENT '备注'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='标准基础信息';

CREATE TABLE IF NOT EXISTS `standard_content` (
  `id` BIGINT NULL DEFAULT NULL COMMENT '主键ID',
  `standard_no` VARCHAR(100) NULL DEFAULT NULL COMMENT '标准号',
  `parent_node_id` BIGINT NULL DEFAULT NULL COMMENT '父节点ID',
  `sibling_order_no` INT NULL DEFAULT NULL COMMENT '同级内排序号',
  `content_level` INT NULL DEFAULT NULL COMMENT '内容层级',
  `source_page_no` INT NULL DEFAULT NULL COMMENT '所在文件页面',
  `clause_no` VARCHAR(100) NULL DEFAULT NULL COMMENT '条款编号',
  `content_type` VARCHAR(100) NULL DEFAULT NULL COMMENT '内容类型（关联文档类型字典）',
  `content_text_with_no` TEXT NULL DEFAULT NULL COMMENT '内容（包含编号）；如出现上标或下标直接存C₂；只有公式占空行，图表存“图x/表x”',
  `is_mandatory` INT NULL DEFAULT NULL COMMENT '是否强制',
  `created_at` DATETIME NULL DEFAULT NULL COMMENT '创建时间',
  `created_by` VARCHAR(64) NULL DEFAULT NULL COMMENT '创建人',
  `updated_at` DATETIME NULL DEFAULT NULL COMMENT '更新时间',
  `updated_by` VARCHAR(64) NULL DEFAULT NULL COMMENT '更新人',
  `is_deleted` INT NULL DEFAULT NULL COMMENT '是否删除',
  `remark` VARCHAR(500) NULL DEFAULT NULL COMMENT '备注'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='标准正文内容';

CREATE TABLE IF NOT EXISTS `document_type` (
  `type_name` VARCHAR(100) NULL DEFAULT NULL COMMENT '类型',
  `sort_no` INT NULL DEFAULT NULL COMMENT '序号',
  `created_at` DATETIME NULL DEFAULT NULL COMMENT '创建时间',
  `created_by` VARCHAR(64) NULL DEFAULT NULL COMMENT '创建人',
  `updated_at` DATETIME NULL DEFAULT NULL COMMENT '更新时间',
  `updated_by` VARCHAR(64) NULL DEFAULT NULL COMMENT '更新人',
  `is_deleted` INT NULL DEFAULT NULL COMMENT '是否删除',
  `remark` VARCHAR(500) NULL DEFAULT NULL COMMENT '备注'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='文档类型';

INSERT INTO `document_type` (`type_name`, `sort_no`, `created_at`, `created_by`, `updated_at`, `updated_by`, `is_deleted`, `remark`)
SELECT '图片', 1, NULL, NULL, NULL, NULL, NULL, NULL
WHERE NOT EXISTS (SELECT 1 FROM `document_type` WHERE `type_name` = '图片');

INSERT INTO `document_type` (`type_name`, `sort_no`, `created_at`, `created_by`, `updated_at`, `updated_by`, `is_deleted`, `remark`)
SELECT '表格', 2, NULL, NULL, NULL, NULL, NULL, NULL
WHERE NOT EXISTS (SELECT 1 FROM `document_type` WHERE `type_name` = '表格');

INSERT INTO `document_type` (`type_name`, `sort_no`, `created_at`, `created_by`, `updated_at`, `updated_by`, `is_deleted`, `remark`)
SELECT '公式', 3, NULL, NULL, NULL, NULL, NULL, NULL
WHERE NOT EXISTS (SELECT 1 FROM `document_type` WHERE `type_name` = '公式');

INSERT INTO `document_type` (`type_name`, `sort_no`, `created_at`, `created_by`, `updated_at`, `updated_by`, `is_deleted`, `remark`)
SELECT '标题', 4, NULL, NULL, NULL, NULL, NULL, NULL
WHERE NOT EXISTS (SELECT 1 FROM `document_type` WHERE `type_name` = '标题');

INSERT INTO `document_type` (`type_name`, `sort_no`, `created_at`, `created_by`, `updated_at`, `updated_by`, `is_deleted`, `remark`)
SELECT '有编号内容', 5, NULL, NULL, NULL, NULL, NULL, NULL
WHERE NOT EXISTS (SELECT 1 FROM `document_type` WHERE `type_name` = '有编号内容');

INSERT INTO `document_type` (`type_name`, `sort_no`, `created_at`, `created_by`, `updated_at`, `updated_by`, `is_deleted`, `remark`)
SELECT '无编号内容', 6, NULL, NULL, NULL, NULL, NULL, NULL
WHERE NOT EXISTS (SELECT 1 FROM `document_type` WHERE `type_name` = '无编号内容');

SET FOREIGN_KEY_CHECKS = 1;
