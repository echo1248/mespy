#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select

from backend.app.mes.crud.prod.crud_yz_mc60_01_test import yz_mc60_01_test_dao
from backend.app.mes.model import YZMC6001Test
from backend.app.mes.schema.prod.yz_mc60_01_test import CreateYZMC6001TestParam, DeleteYZMC6001TestParam
from backend.common.exception import errors
from backend.database.db import async_db_session


class YZMC6001TestService:

    @staticmethod
    async def get(*, pk: int) -> YZMC6001Test:
        async with async_db_session() as db:
            row = await yz_mc60_01_test_dao.get(db, pk)
            if not row:
                raise errors.NotFoundError(msg='数据不存在')
            return row

    @staticmethod
    async def get_select(*, test_snkey: str | None) -> Select:
        return await yz_mc60_01_test_dao.get_list(test_snkey=test_snkey)

    @staticmethod
    async def create(*, obj: CreateYZMC6001TestParam) -> None:
        async with async_db_session.begin() as db:
            await yz_mc60_01_test_dao.create(db, obj)

    @staticmethod
    async def bulk_create(*, objs: list[CreateYZMC6001TestParam]) -> None:
        async with async_db_session.begin() as db:
            await yz_mc60_01_test_dao.bulk_create(db, objs)

    @staticmethod
    async def delete(*, obj: DeleteYZMC6001TestParam) -> int:
        async with async_db_session.begin() as db:
            count = await yz_mc60_01_test_dao.delete(db, obj.pks)
            return count

    @staticmethod
    async def delete_all() -> None:
        async with async_db_session.begin() as db:
            await yz_mc60_01_test_dao.delete_all(db)


yz_mc60_01_test_service: YZMC6001TestService = YZMC6001TestService()
