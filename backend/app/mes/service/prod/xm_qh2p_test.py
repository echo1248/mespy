#!/usr/bin/env python3
from sqlalchemy import Select

from backend.app.mes.crud.prod.crud_xm_qh2p_test import xm_qh2p_test_dao
from backend.app.mes.model import XMQH2PTest
from backend.app.mes.schema.prod.xm_qh2p_test import CreateXMQH2PTestParam, DeleteXMQH2PTestParam
from backend.common.exception import errors
from backend.database.db import async_db_session


class XMQH2PTestService:
    @staticmethod
    async def get(*, pk: int) -> XMQH2PTest:
        async with async_db_session() as db:
            row = await xm_qh2p_test_dao.get(db, pk)
            if not row:
                raise errors.NotFoundError(msg='数据不存在')
            return row

    @staticmethod
    async def get_select(*, test_snkey: str | None) -> Select:
        return await xm_qh2p_test_dao.get_list(test_snkey=test_snkey)

    @staticmethod
    async def create(*, obj: CreateXMQH2PTestParam) -> None:
        async with async_db_session.begin() as db:
            await xm_qh2p_test_dao.create(db, obj)

    @staticmethod
    async def bulk_create(*, objs: list[CreateXMQH2PTestParam]) -> None:
        async with async_db_session.begin() as db:
            await xm_qh2p_test_dao.bulk_create(db, objs)

    @staticmethod
    async def delete(*, obj: DeleteXMQH2PTestParam) -> int:
        async with async_db_session.begin() as db:
            return await xm_qh2p_test_dao.delete(db, obj.pks)

    @staticmethod
    async def delete_all() -> None:
        async with async_db_session.begin() as db:
            await xm_qh2p_test_dao.delete_all(db)


xm_qh2p_test_service: XMQH2PTestService = XMQH2PTestService()
