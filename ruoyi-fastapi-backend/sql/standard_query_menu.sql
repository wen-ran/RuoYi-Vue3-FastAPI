-- 标准查询页面菜单与权限补丁（MySQL）
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
select 1210, '标准查询', 1200, 2, 'query', 'standard/query/index', '', '',
       1, 0, 'C', '0', '0', 'standard:query:list', 'search',
       'admin', sysdate(), '', null, '标准查询菜单'
from dual
where not exists (select 1 from sys_menu where menu_id = 1210);

insert into sys_menu (
  menu_id, menu_name, parent_id, order_num, path, component, query, route_name,
  is_frame, is_cache, menu_type, visible, status, perms, icon,
  create_by, create_time, update_by, update_time, remark
)
select 1211, '标准查询列表', 1210, 1, '#', '', '', '',
       1, 0, 'F', '0', '0', 'standard:query:list', '#',
       'admin', sysdate(), '', null, ''
from dual
where not exists (select 1 from sys_menu where menu_id = 1211);

insert into sys_menu (
  menu_id, menu_name, parent_id, order_num, path, component, query, route_name,
  is_frame, is_cache, menu_type, visible, status, perms, icon,
  create_by, create_time, update_by, update_time, remark
)
select 1212, '标准正文查询', 1210, 2, '#', '', '', '',
       1, 0, 'F', '0', '0', 'standard:query:content', '#',
       'admin', sysdate(), '', null, ''
from dual
where not exists (select 1 from sys_menu where menu_id = 1212);

insert into sys_role_menu (role_id, menu_id)
select 2, 1200
from dual
where exists (select 1 from sys_role where role_id = 2)
  and not exists (select 1 from sys_role_menu where role_id = 2 and menu_id = 1200);

insert into sys_role_menu (role_id, menu_id)
select 2, 1210
from dual
where exists (select 1 from sys_role where role_id = 2)
  and not exists (select 1 from sys_role_menu where role_id = 2 and menu_id = 1210);

insert into sys_role_menu (role_id, menu_id)
select 2, 1211
from dual
where exists (select 1 from sys_role where role_id = 2)
  and not exists (select 1 from sys_role_menu where role_id = 2 and menu_id = 1211);

insert into sys_role_menu (role_id, menu_id)
select 2, 1212
from dual
where exists (select 1 from sys_role where role_id = 2)
  and not exists (select 1 from sys_role_menu where role_id = 2 and menu_id = 1212);
