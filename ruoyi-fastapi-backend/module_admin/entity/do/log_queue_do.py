from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, Index, Integer, String, Text

from config.database import Base


class SysLogQueue(Base):
    """
    日志队列
    """

    __tablename__ = 'sys_log_queue'
    __table_args__ = {'comment': '日志队列'}

    queue_id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True, comment='队列ID')
    event_id = Column(String(64), nullable=False, unique=True, comment='事件唯一ID')
    event_type = Column(String(32), nullable=False, comment='事件类型')
    payload = Column(Text, nullable=False, comment='事件内容')
    source = Column(String(64), nullable=True, comment='事件来源')
    status = Column(String(16), nullable=False, server_default='pending', comment='状态')
    locked_by = Column(String(64), nullable=True, comment='锁定者')
    locked_until = Column(DateTime, nullable=True, comment='锁定到期')
    attempt_count = Column(Integer, nullable=False, server_default='0', comment='重试次数')
    last_error = Column(String(500), nullable=True, comment='最后错误')
    create_time = Column(DateTime, nullable=True, default=datetime.now(), comment='创建时间')
    update_time = Column(DateTime, nullable=True, default=datetime.now(), comment='更新时间')
    processed_time = Column(DateTime, nullable=True, comment='处理时间')

    idx_sys_log_queue_status = Index('idx_sys_log_queue_status', status)
    idx_sys_log_queue_locked_until = Index('idx_sys_log_queue_locked_until', locked_until)
    idx_sys_log_queue_create_time = Index('idx_sys_log_queue_create_time', create_time)
