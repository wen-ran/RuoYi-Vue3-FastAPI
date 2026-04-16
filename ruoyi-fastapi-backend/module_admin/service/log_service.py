import asyncio
import hashlib
import json
import uuid
from typing import Any

from fastapi import Request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import CrudResponseModel, PageModel
from config.database import AsyncSessionLocal
from config.env import LogConfig
from exceptions.exception import ServiceException
from middlewares.trace_middleware.ctx import TraceCtx
from module_admin.dao.log_dao import LoginLogDao, OperationLogDao
from module_admin.dao.log_queue_dao import LogQueueDao
from module_admin.entity.do.log_queue_do import SysLogQueue
from module_admin.entity.vo.log_vo import (
    DeleteLoginLogModel,
    DeleteOperLogModel,
    LogininforModel,
    LoginLogPageQueryModel,
    OperLogModel,
    OperLogPageQueryModel,
    UnlockUser,
)
from module_admin.service.dict_service import DictDataService
from utils.cache_store import CacheStore
from utils.excel_util import ExcelUtil
from utils.log_util import logger


class OperationLogService:
    @classmethod
    async def get_operation_log_list_services(
        cls, query_db: AsyncSession, query_object: OperLogPageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        return await OperationLogDao.get_operation_log_list(query_db, query_object, is_page)

    @classmethod
    async def add_operation_log_services(cls, query_db: AsyncSession, page_object: OperLogModel) -> CrudResponseModel:
        try:
            await OperationLogDao.add_operation_log_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def delete_operation_log_services(
        cls, query_db: AsyncSession, page_object: DeleteOperLogModel
    ) -> CrudResponseModel:
        if not page_object.oper_ids:
            raise ServiceException(message='传入操作日志id为空')

        oper_id_list = page_object.oper_ids.split(',')
        try:
            for oper_id in oper_id_list:
                await OperationLogDao.delete_operation_log_dao(query_db, OperLogModel(operId=oper_id))
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='删除成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def clear_operation_log_services(cls, query_db: AsyncSession) -> CrudResponseModel:
        try:
            await OperationLogDao.clear_operation_log_dao(query_db)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='清空成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def export_operation_log_list_services(cls, request: Request, operation_log_list: list) -> bytes:
        mapping_dict = {
            'operId': '日志编号',
            'title': '系统模块',
            'businessType': '操作类型',
            'method': '方法名称',
            'requestMethod': '请求方式',
            'operName': '操作人员',
            'deptName': '部门名称',
            'operUrl': '请求URL',
            'operIp': '操作地址',
            'operLocation': '操作地点',
            'operParam': '请求参数',
            'jsonResult': '返回参数',
            'status': '操作状态',
            'error_msg': '错误消息',
            'operTime': '操作日期',
            'costTime': '消耗时间（毫秒）',
        }

        operation_type_list = await DictDataService.query_dict_data_list_from_cache_services(
            request.app.state.redis, dict_type='sys_oper_type'
        )
        operation_type_option = [
            {'label': item.get('dictLabel'), 'value': item.get('dictValue')} for item in operation_type_list
        ]
        operation_type_option_dict = {item.get('value'): item for item in operation_type_option}

        for item in operation_log_list:
            item['status'] = '成功' if item.get('status') == 0 else '失败'
            if str(item.get('businessType')) in operation_type_option_dict:
                item['businessType'] = operation_type_option_dict.get(str(item.get('businessType'))).get('label')

        return ExcelUtil.export_list2excel(operation_log_list, mapping_dict)


class LoginLogService:
    @classmethod
    async def get_login_log_list_services(
        cls, query_db: AsyncSession, query_object: LoginLogPageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        return await LoginLogDao.get_login_log_list(query_db, query_object, is_page)

    @classmethod
    async def add_login_log_services(cls, query_db: AsyncSession, page_object: LogininforModel) -> CrudResponseModel:
        try:
            await LoginLogDao.add_login_log_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def delete_login_log_services(
        cls, query_db: AsyncSession, page_object: DeleteLoginLogModel
    ) -> CrudResponseModel:
        if not page_object.info_ids:
            raise ServiceException(message='传入登录日志id为空')

        info_id_list = page_object.info_ids.split(',')
        try:
            for info_id in info_id_list:
                await LoginLogDao.delete_login_log_dao(query_db, LogininforModel(infoId=info_id))
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='删除成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def clear_login_log_services(cls, query_db: AsyncSession) -> CrudResponseModel:
        try:
            await LoginLogDao.clear_login_log_dao(query_db)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='清空成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def unlock_user_services(cls, request: Request, unlock_user: UnlockUser) -> CrudResponseModel:
        locked_user = await request.app.state.redis.get(f'account_lock:{unlock_user.user_name}')
        if locked_user:
            await request.app.state.redis.delete(f'account_lock:{unlock_user.user_name}')
            return CrudResponseModel(is_success=True, message='解锁成功')
        raise ServiceException(message='该用户未锁定')

    @staticmethod
    async def export_login_log_list_services(login_log_list: list) -> bytes:
        mapping_dict = {
            'infoId': '访问编号',
            'userName': '用户名称',
            'ipaddr': '登录地址',
            'loginLocation': '登录地点',
            'browser': '浏览器',
            'os': '操作系统',
            'status': '登录状态',
            'msg': '操作信息',
            'loginTime': '登录日期',
        }

        for item in login_log_list:
            item['status'] = '成功' if item.get('status') == '0' else '失败'

        return ExcelUtil.export_list2excel(login_log_list, mapping_dict)


class LogQueueService:
    @classmethod
    def _build_event_id(cls, request_id: str, log_type: str, source: str) -> str:
        if not request_id:
            return uuid.uuid4().hex
        return hashlib.md5(f'{request_id}:{log_type}:{source}'.encode('utf-8')).hexdigest()

    @classmethod
    async def _enqueue_event(cls, event_type: str, payload: dict, source: str) -> None:
        request_id = TraceCtx.get_request_id()
        trace_id = TraceCtx.get_trace_id()
        span_id = TraceCtx.get_span_id()
        event_id = cls._build_event_id(request_id, event_type, source)
        queue_source = ':'.join(part for part in [source, trace_id, span_id] if part)

        async with AsyncSessionLocal() as session:
            try:
                await LogQueueDao.enqueue(
                    session,
                    SysLogQueue(
                        event_id=event_id,
                        event_type=event_type,
                        payload=json.dumps(payload, ensure_ascii=False, default=str),
                        source=queue_source or source,
                    ),
                )
                await session.commit()
            except IntegrityError:
                await session.rollback()

    @classmethod
    async def enqueue_login_log(cls, request: Request, login_log: LogininforModel, source: str) -> None:
        del request
        payload = login_log.model_dump(by_alias=True, exclude_none=True)
        await cls._enqueue_event('login', payload, source)

    @classmethod
    async def enqueue_operation_log(cls, request: Request, operation_log: OperLogModel, source: str) -> None:
        del request
        payload = operation_log.model_dump(by_alias=True, exclude_none=True)
        await cls._enqueue_event('operation', payload, source)


class LogAggregatorService:
    @classmethod
    async def _process_event(cls, session: AsyncSession, event: dict[str, Any]) -> None:
        payload = json.loads(event.get('payload') or '{}')
        event_type = event.get('event_type')
        if event_type == 'login':
            await LoginLogDao.add_login_log_dao(session, LogininforModel(**payload))
            return
        if event_type == 'operation':
            await OperationLogDao.add_operation_log_dao(session, OperLogModel(**payload))
            return
        raise ServiceException(message=f'不支持的日志事件类型: {event_type}')

    @classmethod
    async def consume_stream(cls, redis: CacheStore) -> None:
        del redis
        consumer_name = f'{LogConfig.log_stream_consumer_prefix}-{uuid.uuid4().hex[:6]}'
        lock_seconds = max(int(LogConfig.log_stream_claim_idle_ms / 1000), 30)
        sleep_seconds = max(LogConfig.log_stream_block_ms / 1000, 0.5)

        while True:
            try:
                async with AsyncSessionLocal() as session:
                    events = await LogQueueDao.claim_events(
                        session,
                        limit=LogConfig.log_stream_batch_size,
                        worker_id=consumer_name,
                        lock_seconds=lock_seconds,
                    )
                    await session.commit()

                if not events:
                    await asyncio.sleep(sleep_seconds)
                    continue

                success_ids: list[int] = []
                failed_events: list[tuple[int, str]] = []

                for event in events:
                    queue_id = int(event['queue_id'])
                    async with AsyncSessionLocal() as session:
                        try:
                            await cls._process_event(session, event)
                            await session.commit()
                            success_ids.append(queue_id)
                        except Exception as exc:
                            await session.rollback()
                            failed_events.append((queue_id, str(exc)))

                if success_ids:
                    async with AsyncSessionLocal() as session:
                        await LogQueueDao.mark_done(session, success_ids)
                        await session.commit()

                for queue_id, error_message in failed_events:
                    async with AsyncSessionLocal() as session:
                        await LogQueueDao.mark_failed(session, [queue_id], error_message)
                        await session.commit()
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                logger.error(f'日志聚合消费异常: {exc}')
                await asyncio.sleep(1)
