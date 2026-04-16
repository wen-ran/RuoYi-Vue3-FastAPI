from fastapi import FastAPI

from config.database import AsyncSessionLocal
from module_admin.service.config_service import ConfigService
from module_admin.service.dict_service import DictDataService
from utils.cache_store import CacheStore
from utils.log_util import logger


class RedisUtil:
    """
    兼容旧调用名称的缓存初始化工具。
    """

    @classmethod
    async def create_redis_pool(cls, log_enabled: bool = True, log_start_enabled: bool | None = None) -> CacheStore:
        """
        应用启动时初始化 MySQL 缓存存储。

        :param log_enabled: 是否输出日志
        :param log_start_enabled: 是否输出开始连接日志
        :return: 缓存连接对象
        """
        redis = CacheStore()
        if log_start_enabled is None:
            log_start_enabled = log_enabled
        if log_enabled or log_start_enabled:
            await cls.check_redis_connection(redis, log_enabled=log_enabled, log_start_enabled=log_start_enabled)
        return redis

    @classmethod
    async def check_redis_connection(
        cls, redis: CacheStore, log_enabled: bool = True, log_start_enabled: bool | None = None
    ) -> None:
        """
        检查缓存连接状态。

        :param redis: 缓存对象
        :param log_enabled: 是否输出日志
        :param log_start_enabled: 是否输出开始连接日志
        :return: None
        """
        if log_start_enabled is None:
            log_start_enabled = log_enabled
        if log_start_enabled:
            logger.info('🔎 开始初始化 MySQL 缓存存储...')

        connection = await redis.ping()
        if not log_enabled:
            return

        if connection:
            logger.info('✅️ MySQL 缓存存储初始化成功')
        else:
            logger.error('❌️ MySQL 缓存存储初始化失败')

    @classmethod
    async def close_redis_pool(cls, app: FastAPI) -> None:
        """
        应用关闭时关闭缓存连接。

        :param app: fastapi对象
        :return: None
        """
        await app.state.redis.close()
        logger.info('✅️ 关闭 MySQL 缓存存储成功')

    @classmethod
    async def init_sys_dict(cls, redis: CacheStore) -> None:
        """
        应用启动时缓存字典表。

        :param redis: 缓存对象
        :return: None
        """
        async with AsyncSessionLocal() as session:
            await DictDataService.init_cache_sys_dict_services(session, redis)

    @classmethod
    async def init_sys_config(cls, redis: CacheStore) -> None:
        """
        应用启动时缓存参数配置表。

        :param redis: 缓存对象
        :return: None
        """
        async with AsyncSessionLocal() as session:
            await ConfigService.init_cache_sys_config_services(session, redis)
