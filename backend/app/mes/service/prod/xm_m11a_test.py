#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select

from backend.app.mes.crud.prod.crud_xm_m11a_test import xm_m11a_test_dao
from backend.app.mes.model import XMM11ATest
from backend.app.mes.schema.prod.xm_m11a_test import CreateXMM11ATestParam, DeleteXMM11ATestParam
from backend.common.exception import errors
from backend.database.db import async_db_session


class XMM11ATestService:

    @staticmethod
    async def get(*, pk: int) -> XMM11ATest:
        async with async_db_session() as db:
            row = await xm_m11a_test_dao.get(db, pk)
            if not row:
                raise errors.NotFoundError(msg='数据不存在')
            return row

    @staticmethod
    async def get_select(*, test_snkey: str | None) -> Select:
        return await xm_m11a_test_dao.get_list(test_snkey=test_snkey)

    @staticmethod
    async def create(*, obj: CreateXMM11ATestParam) -> None:
        async with async_db_session.begin() as db:
            await xm_m11a_test_dao.create(db, obj)

    @staticmethod
    async def bulk_create(*, objs: list[CreateXMM11ATestParam]) -> None:
        async with async_db_session.begin() as db:
            await xm_m11a_test_dao.bulk_create(db, objs)

    @staticmethod
    async def delete(*, obj: DeleteXMM11ATestParam) -> int:
        async with async_db_session.begin() as db:
            count = await xm_m11a_test_dao.delete(db, obj.pks)
            return count

    @staticmethod
    async def delete_all() -> None:
        async with async_db_session.begin() as db:
            await xm_m11a_test_dao.delete_all(db)


xm_m11a_test_service: XMM11ATestService = XMM11ATestService()
