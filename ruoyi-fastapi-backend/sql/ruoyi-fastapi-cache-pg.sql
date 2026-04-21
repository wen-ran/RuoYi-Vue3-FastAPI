-- ----------------------------
-- PostgreSQL 缓存与日志队列表
-- ----------------------------

drop table if exists sys_cache;
create table sys_cache (
  cache_key     varchar(191) primary key,
  cache_value   text,
  expire_at     timestamp,
  create_time   timestamp default current_timestamp,
  update_time   timestamp default current_timestamp
);
comment on table sys_cache is '系统缓存键值表';
comment on column sys_cache.cache_key is '缓存键';
comment on column sys_cache.cache_value is '缓存值';
comment on column sys_cache.expire_at is '过期时间';
comment on column sys_cache.create_time is '创建时间';
comment on column sys_cache.update_time is '更新时间';
create index idx_sys_cache_expire_at on sys_cache (expire_at);


drop table if exists sys_log_queue;
create table sys_log_queue (
  queue_id       bigserial primary key,
  event_id       varchar(64) not null unique,
  event_type     varchar(32) not null,
  payload        text not null,
  source         varchar(64),
  status         varchar(16) not null default 'pending',
  locked_by      varchar(64),
  locked_until   timestamp,
  attempt_count  integer not null default 0,
  last_error     varchar(500),
  create_time    timestamp default current_timestamp,
  update_time    timestamp default current_timestamp,
  processed_time timestamp
);
comment on table sys_log_queue is '日志队列表';
comment on column sys_log_queue.queue_id is '队列ID';
comment on column sys_log_queue.event_id is '事件唯一ID';
comment on column sys_log_queue.event_type is '事件类型';
comment on column sys_log_queue.payload is '事件内容';
comment on column sys_log_queue.source is '事件来源';
comment on column sys_log_queue.status is '状态';
comment on column sys_log_queue.locked_by is '锁定者';
comment on column sys_log_queue.locked_until is '锁定到期';
comment on column sys_log_queue.attempt_count is '重试次数';
comment on column sys_log_queue.last_error is '最后错误';
comment on column sys_log_queue.create_time is '创建时间';
comment on column sys_log_queue.update_time is '更新时间';
comment on column sys_log_queue.processed_time is '处理时间';
create index idx_sys_log_queue_status on sys_log_queue (status);
create index idx_sys_log_queue_locked_until on sys_log_queue (locked_until);
create index idx_sys_log_queue_create_time on sys_log_queue (create_time);
