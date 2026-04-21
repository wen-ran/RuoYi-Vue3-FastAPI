-- 标准上传页面菜单与权限补丁（MySQL）
-- 如已有对应 menu_id，本脚本会跳过插入。

insert into sys_menu (
  menu_id, menu_name, parent_id, order_num, path, component, query, route_name,
  is_frame, is_cache, menu_type, visible, status, perms, icon,
  create_by, create_time, update_by, update_time, remark
)
select 1200, '标准管理', 0, 5, 'standard', null, '', '',
       1, 0, 'M', '0', '0', '', 'education',
       'admin', sysdate(), '', null, '标准管理目录'
from dual
where not exists (select 1 from sys_menu where menu_id = 1200);

insert into sys_menu (
  menu_id, menu_name, parent_id, order_num, path, component, query, route_name,
  is_frame, is_cache, menu_type, visible, status, perms, icon,
  create_by, create_time, update_by, update_time, remark
)
select 1201, '标准上传', 1200, 1, 'upload', 'standard/upload/index', '', '',
       1, 0, 'C', '0', '0', 'standard:upload:list', 'upload',
       'admin', sysdate(), '', null, '标准上传菜单'
from dual
where not exists (select 1 from sys_menu where menu_id = 1201);

insert into sys_menu (
  menu_id, menu_name, parent_id, order_num, path, component, query, route_name,
  is_frame, is_cache, menu_type, visible, status, perms, icon,
  create_by, create_time, update_by, update_time, remark
)
select 1202, '标准上传查询', 1201, 1, '#', '', '', '',
       1, 0, 'F', '0', '0', 'standard:upload:list', '#',
       'admin', sysdate(), '', null, ''
from dual
where not exists (select 1 from sys_menu where menu_id = 1202);

insert into sys_menu (
  menu_id, menu_name, parent_id, order_num, path, component, query, route_name,
  is_frame, is_cache, menu_type, visible, status, perms, icon,
  create_by, create_time, update_by, update_time, remark
)
select 1203, '标准文件上传', 1201, 2, '#', '', '', '',
       1, 0, 'F', '0', '0', 'standard:upload:file', '#',
       'admin', sysdate(), '', null, ''
from dual
where not exists (select 1 from sys_menu where menu_id = 1203);

insert into sys_role_menu (role_id, menu_id)
select 2, 1200
from dual
where exists (select 1 from sys_role where role_id = 2)
  and not exists (select 1 from sys_role_menu where role_id = 2 and menu_id = 1200);

insert into sys_role_menu (role_id, menu_id)
select 2, 1201
from dual
where exists (select 1 from sys_role where role_id = 2)
  and not exists (select 1 from sys_role_menu where role_id = 2 and menu_id = 1201);

insert into sys_role_menu (role_id, menu_id)
select 2, 1202
from dual
where exists (select 1 from sys_role where role_id = 2)
  and not exists (select 1 from sys_role_menu where role_id = 2 and menu_id = 1202);

insert into sys_role_menu (role_id, menu_id)
select 2, 1203
from dual
where exists (select 1 from sys_role where role_id = 2)
  and not exists (select 1 from sys_role_menu where role_id = 2 and menu_id = 1203);
