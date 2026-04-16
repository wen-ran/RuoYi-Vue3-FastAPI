from __future__ import annotations

import asyncio
from datetime import datetime, timedelta
from sqlalchemy import delete, func, or_, select, update

from config.database import AsyncSessionLocal
from module_admin.entity.do.cache_do import SysCache


class CachePubSub:
    """
    基于 MySQL 缓存表的轻量发布订阅兼容层。

    这里只用于调度同步信号，不保证完整的 Redis Pub/Sub 语义。
    """

    def __init__(self, store: 'CacheStore') -> None:
        self._store = store
        self._channels: set[str] = set()
        self._last_messages: dict[str, str | None] = {}
        self._closed = False

    async def subscribe(self, *channels: str) -> None:
        for channel in channels:
            self._channels.add(channel)
            self._last_messages[channel] = await self._store.get(self._store._pubsub_key(channel))

    async def unsubscribe(self, *channels: str) -> None:
        if channels:
            for channel in channels:
                self._channels.discard(channel)
                self._last_messages.pop(channel, None)
            return
        self._channels.clear()
        self._last_messages.clear()

    async def listen(self):
        while not self._closed:
            delivered = False
            for channel in list(self._channels):
                current = await self._store.get(self._store._pubsub_key(channel))
                if current is None or current == self._last_messages.get(channel):
                    continue
                self._last_messages[channel] = current
                delivered = True
                yield {'type': 'message', 'channel': channel, 'data': current}
            if not delivered:
                await asyncio.sleep(0.5)

    async def close(self) -> None:
        self._closed = True
        await self.unsubscribe()


class CacheStore:
    """
    基于MySQL的缓存存储，提供Redis风格的常用接口。
    """

    def __init__(self, namespace: str | None = None) -> None:
        self._namespace = namespace or ''

    def _apply_namespace(self, key: str) -> str:
        if not self._namespace:
            return key
        return f'{self._namespace}:{key}'

    @staticmethod
    def _pubsub_key(channel: str) -> str:
        return f'__pubsub__:{channel}'

    @staticmethod
    def _now() -> datetime:
        return datetime.now()

    @staticmethod
    def _parse_expire(ex: int | timedelta | None) -> datetime | None:
        if ex is None:
            return None
        if isinstance(ex, timedelta):
            return CacheStore._now() + ex
        return CacheStore._now() + timedelta(seconds=int(ex))

    @staticmethod
    def _to_like_pattern(pattern: str) -> tuple[str, str]:
        escape_char = '\\'
        escaped = (
            pattern.replace(escape_char, f'{escape_char}{escape_char}')
            .replace('%', f'{escape_char}%')
            .replace('_', f'{escape_char}_')
        )
        return escaped.replace('*', '%'), escape_char

    async def ping(self) -> bool:
        return True

    async def close(self) -> None:
        return None

    async def publish(self, channel: str, message: str) -> int:
        await self.set(self._pubsub_key(channel), str(message), ex=timedelta(minutes=5))
        return 1

    def pubsub(self) -> CachePubSub:
        return CachePubSub(self)

    async def get(self, key: str) -> str | None:
        cache_key = self._apply_namespace(key)
        now = self._now()
        async with AsyncSessionLocal() as session:
            row = (
                await session.execute(
                    select(SysCache).where(
                        SysCache.cache_key == cache_key,
                        or_(SysCache.expire_at.is_(None), SysCache.expire_at > now),
                    )
                )
            ).scalars().first()
            if row:
                return row.cache_value
            await session.execute(
                delete(SysCache).where(SysCache.cache_key == cache_key, SysCache.expire_at <= now)
            )
            await session.commit()
        return None

    async def set(self, key: str, value: str, ex: int | timedelta | None = None, nx: bool = False) -> bool:
        cache_key = self._apply_namespace(key)
        expire_at = self._parse_expire(ex)
        now = self._now()
        value = str(value)
        async with AsyncSessionLocal() as session:
            existing = (
                await session.execute(select(SysCache).where(SysCache.cache_key == cache_key))
            ).scalars().first()
            if existing and existing.expire_at and existing.expire_at <= now:
                await session.delete(existing)
                await session.flush()
                existing = None
            if nx and existing:
                return False
            if existing:
                await session.execute(
                    update(SysCache)
                    .where(SysCache.cache_key == cache_key)
                    .values(cache_value=value, expire_at=expire_at, update_time=now)
                )
            else:
                session.add(
                    SysCache(
                        cache_key=cache_key,
                        cache_value=value,
                        expire_at=expire_at,
                        create_time=now,
                        update_time=now,
                    )
                )
            await session.commit()
        return True

    async def delete(self, *keys: str) -> int:
        if not keys:
            return 0
        cache_keys = [self._apply_namespace(key) for key in keys]
        async with AsyncSessionLocal() as session:
            result = await session.execute(delete(SysCache).where(SysCache.cache_key.in_(cache_keys)))
            await session.commit()
            return result.rowcount or 0

    async def expire(self, key: str, ex: int | timedelta) -> bool:
        cache_key = self._apply_namespace(key)
        expire_at = self._parse_expire(ex)
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                update(SysCache).where(SysCache.cache_key == cache_key).values(expire_at=expire_at)
            )
            await session.commit()
            return bool(result.rowcount)

    async def keys(self, pattern: str | None = None) -> list[str]:
        now = self._now()
        if not pattern:
            pattern = '*'
        cache_pattern = self._apply_namespace(pattern)
        like_pattern, escape_char = self._to_like_pattern(cache_pattern)
        async with AsyncSessionLocal() as session:
            rows = (
                await session.execute(
                    select(SysCache.cache_key).where(
                        SysCache.cache_key.like(like_pattern, escape=escape_char),
                        or_(SysCache.expire_at.is_(None), SysCache.expire_at > now),
                    )
                )
            ).scalars().all()
            if self._namespace:
                prefix = f'{self._namespace}:'
                return [key[len(prefix) :] for key in rows if key.startswith(prefix)]
            return list(rows)

    async def dbsize(self) -> int:
        now = self._now()
        async with AsyncSessionLocal() as session:
            count = (
                await session.execute(
                    select(func.count()).select_from(SysCache).where(
                        or_(SysCache.expire_at.is_(None), SysCache.expire_at > now)
                    )
                )
            ).scalar_one()
        return int(count or 0)

    async def info(self, section: str | None = None) -> dict:
        if section == 'commandstats':
            return {}
        return {
            'cache_type': 'mysql',
            'cache_table': SysCache.__tablename__,
            'keys': await self.dbsize(),
        }
