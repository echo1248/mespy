#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select

from backend.app.mes.crud.prod.crud_yz_mc601_test import yz_mc601_test_dao
from backend.app.mes.model import YZMC601Test
from backend.app.mes.schema.prod.yz_mc601_test import CreateYZMC601TestParam, DeleteYZMC601TestParam
from backend.common.exception import errors
from backend.database.db import async_db_session


class YZMC601TestService:

    @staticmethod
    async def get(*, pk: int) -> YZMC601Test:
        async with async_db_session() as db:
            row = await yz_mc601_test_dao.get(db, pk)
            if not row:
                raise errors.NotFoundError(msg='数据不存在')
            return row

    @staticmethod
    async def get_select(*, test_snkey: str | None) -> Select:
        return await yz_mc601_test_dao.get_list(test_snkey=test_snkey)

    @staticmethod
    async def create(*, obj: CreateYZMC601TestParam) -> None:
        async with async_db_session.begin() as db:
            await yz_mc601_test_dao.create(db, obj)

    @staticmethod
    async def bulk_create(*, objs: list[CreateYZMC601TestParam]) -> None:
        async with async_db_session.begin() as db:
            await yz_mc601_test_dao.bulk_create(db, objs)

    @staticmethod
    async def delete(*, obj: DeleteYZMC601TestParam) -> int:
        async with async_db_session.begin() as db:
            count = await yz_mc601_test_dao.delete(db, obj.pks)
            return count

    @staticmethod
    async def delete_all() -> None:
        async with async_db_session.begin() as db:
            await yz_mc601_test_dao.delete_all(db)


yz_mc601_test_service: YZMC601TestService = YZMC601TestService()
