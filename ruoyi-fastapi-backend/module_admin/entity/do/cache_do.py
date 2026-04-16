from datetime import datetime

from sqlalchemy import Column, DateTime, Index, String, Text

from config.database import Base


class SysCache(Base):
    """
    系统缓存键值
    """

    __tablename__ = 'sys_cache'
    __table_args__ = {'comment': '系统缓存键值'}

    cache_key = Column(String(191), primary_key=True, nullable=False, comment='缓存键')
    cache_value = Column(Text, nullable=True, comment='缓存值')
    expire_at = Column(DateTime, nullable=True, comment='过期时间')
    create_time = Column(DateTime, nullable=True, default=datetime.now(), comment='创建时间')
    update_time = Column(DateTime, nullable=True, default=datetime.now(), comment='更新时间')

    idx_sys_cache_expire_at = Index('idx_sys_cache_expire_at', expire_at)
