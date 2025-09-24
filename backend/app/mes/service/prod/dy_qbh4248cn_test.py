#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select

from backend.app.mes.crud.prod.crud_dy_qbh4248cn_test import dy_qbh4248cn_test_dao
from backend.app.mes.model import DyQBH4248CNTest
from backend.app.mes.schema.prod.dy_qbh4248cn_test import CreateDyQBH4248CNTestParam, DeleteDyQBH4248CNTestParam
from backend.common.exception import errors
from backend.database.db import async_db_session


class DyQBH4248CNTestService:

    @staticmethod
    async def get(*, pk: int) -> DyQBH4248CNTest:
        async with async_db_session() as db:
            row = await dy_qbh4248cn_test_dao.get(db, pk)
            if not row:
                raise errors.NotFoundError(msg='数据不存在')
            return row

    @staticmethod
    async def get_select(*, test_sn: str | None) -> Select:
        return await dy_qbh4248cn_test_dao.get_list(test_sn=test_sn)

    @staticmethod
    async def create(*, obj: CreateDyQBH4248CNTestParam) -> None:
        async with async_db_session.begin() as db:
            await dy_qbh4248cn_test_dao.create(db, obj)

    @staticmethod
    async def bulk_create(*, objs: list[CreateDyQBH4248CNTestParam]) -> None:
        async with async_db_session.begin() as db:
            await dy_qbh4248cn_test_dao.bulk_create(db, objs)

    @staticmethod
    async def delete(*, obj: DeleteDyQBH4248CNTestParam) -> int:
        async with async_db_session.begin() as db:
            count = await dy_qbh4248cn_test_dao.delete(db, obj.pks)
            return count

    @staticmethod
    async def delete_all() -> None:
        async with async_db_session.begin() as db:
            await dy_qbh4248cn_test_dao.delete_all(db)


dy_qbh4248cn_test_service: DyQBH4248CNTestService = DyQBH4248CNTestService()
