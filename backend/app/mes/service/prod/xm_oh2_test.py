#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select

from backend.app.mes.crud.prod.crud_xm_oh2_test import xm_oh2_test_dao
from backend.app.mes.model import XMOH2Test
from backend.app.mes.schema.prod.xm_oh2_test import CreateXMOH2TestParam, DeleteXMOH2TestParam
from backend.common.exception import errors
from backend.database.db import async_db_session


class XMOH2TestService:

    @staticmethod
    async def get(*, pk: int) -> XMOH2Test:
        async with async_db_session() as db:
            row = await xm_oh2_test_dao.get(db, pk)
            if not row:
                raise errors.NotFoundError(msg='数据不存在')
            return row

    @staticmethod
    async def get_select(*, test_snkey: str | None) -> Select:
        return await xm_oh2_test_dao.get_list(test_snkey=test_snkey)

    @staticmethod
    async def create(*, obj: CreateXMOH2TestParam) -> None:
        async with async_db_session.begin() as db:
            await xm_oh2_test_dao.create(db, obj)

    @staticmethod
    async def bulk_create(*, objs: list[CreateXMOH2TestParam]) -> None:
        async with async_db_session.begin() as db:
            await xm_oh2_test_dao.bulk_create(db, objs)

    @staticmethod
    async def delete(*, obj: DeleteXMOH2TestParam) -> int:
        async with async_db_session.begin() as db:
            count = await xm_oh2_test_dao.delete(db, obj.pks)
            return count

    @staticmethod
    async def delete_all() -> None:
        async with async_db_session.begin() as db:
            await xm_oh2_test_dao.delete_all(db)


xm_oh2_test_service: XMOH2TestService = XMOH2TestService()
