#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select

from backend.app.mes.crud.prod.crud_xm_ph3rm_test import xm_ph3rm_test_dao
from backend.app.mes.model import XMPH3RMTest
from backend.app.mes.schema.prod.xm_ph3rm_test import CreateXMPH3RMTestParam, DeleteXMPH3RMTestParam
from backend.common.exception import errors
from backend.database.db import async_db_session


class XMPH3RMTestService:

    @staticmethod
    async def get(*, pk: int) -> XMPH3RMTest:
        async with async_db_session() as db:
            row = await xm_ph3rm_test_dao.get(db, pk)
            if not row:
                raise errors.NotFoundError(msg='数据不存在')
            return row

    @staticmethod
    async def get_select(*, test_snkey: str | None) -> Select:
        return await xm_ph3rm_test_dao.get_list(test_snkey=test_snkey)

    @staticmethod
    async def create(*, obj: CreateXMPH3RMTestParam) -> None:
        async with async_db_session.begin() as db:
            await xm_ph3rm_test_dao.create(db, obj)

    @staticmethod
    async def bulk_create(*, objs: list[CreateXMPH3RMTestParam]) -> None:
        async with async_db_session.begin() as db:
            await xm_ph3rm_test_dao.bulk_create(db, objs)

    @staticmethod
    async def delete(*, obj: DeleteXMPH3RMTestParam) -> int:
        async with async_db_session.begin() as db:
            count = await xm_ph3rm_test_dao.delete(db, obj.pks)
            return count

    @staticmethod
    async def delete_all() -> None:
        async with async_db_session.begin() as db:
            await xm_ph3rm_test_dao.delete_all(db)


xm_ph3rm_test_service: XMPH3RMTestService = XMPH3RMTestService()
