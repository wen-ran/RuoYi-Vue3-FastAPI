from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import and_, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from module_admin.entity.do.log_queue_do import SysLogQueue


class LogQueueDao:
    """
    日志队列数据访问
    """

    @classmethod
    async def enqueue(cls, db: AsyncSession, log_event: SysLogQueue) -> None:
        db.add(log_event)
        await db.flush()

    @classmethod
    async def claim_events(
        cls, db: AsyncSession, limit: int, worker_id: str, lock_seconds: int
    ) -> list[dict[str, Any]]:
        now = datetime.now()
        lock_until = now + timedelta(seconds=lock_seconds)
        claimed_rows: list[dict[str, Any]] = []
        visited_ids: set[int] = set()

        while len(claimed_rows) < limit:
            query = (
                select(SysLogQueue)
                .where(
                    or_(
                        SysLogQueue.status == 'pending',
                        and_(SysLogQueue.status == 'processing', SysLogQueue.locked_until < now),
                    ),
                    SysLogQueue.queue_id.not_in(visited_ids) if visited_ids else True,
                )
                .order_by(SysLogQueue.queue_id)
                .limit(max(limit - len(claimed_rows), 10))
            )
            rows = (await db.execute(query)).scalars().all()
            if not rows:
                break

            for row in rows:
                visited_ids.add(row.queue_id)
                result = await db.execute(
                    update(SysLogQueue)
                    .where(
                        SysLogQueue.queue_id == row.queue_id,
                        or_(
                            SysLogQueue.status == 'pending',
                            and_(SysLogQueue.status == 'processing', SysLogQueue.locked_until < now),
                        ),
                    )
                    .values(
                        status='processing',
                        locked_by=worker_id,
                        locked_until=lock_until,
                        update_time=now,
                    )
                )
                if not result.rowcount:
                    continue

                row.status = 'processing'
                row.locked_by = worker_id
                row.locked_until = lock_until
                row.update_time = now
                claimed_rows.append(
                    {
                        'queue_id': row.queue_id,
                        'event_type': row.event_type,
                        'payload': row.payload,
                    }
                )
                if len(claimed_rows) >= limit:
                    break

        await db.flush()
        return claimed_rows

    @classmethod
    async def mark_done(cls, db: AsyncSession, queue_ids: list[int]) -> None:
        if not queue_ids:
            return
        now = datetime.now()
        await db.execute(
            update(SysLogQueue)
            .where(SysLogQueue.queue_id.in_(queue_ids))
            .values(status='done', locked_by=None, locked_until=None, processed_time=now, update_time=now)
        )

    @classmethod
    async def mark_failed(cls, db: AsyncSession, queue_ids: list[int], error_message: str) -> None:
        if not queue_ids:
            return
        now = datetime.now()
        await db.execute(
            update(SysLogQueue)
            .where(SysLogQueue.queue_id.in_(queue_ids))
            .values(
                status='pending',
                locked_by=None,
                locked_until=None,
                attempt_count=SysLogQueue.attempt_count + 1,
                last_error=error_message[:500],
                update_time=now,
            )
        )
