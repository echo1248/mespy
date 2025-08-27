#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select

from backend.app.mes.crud.prod.crud_jr_jm03_test import jr_jm03_test_dao
from backend.app.mes.model import JRJM03Test
from backend.app.mes.schema.prod.jr_jm03_test import CreateJRJM03TestParam, DeleteJRJM03TestParam
from backend.common.exception import errors
from backend.database.db import async_db_session


class JRJM03TestService:

    @staticmethod
    async def get(*, pk: int) -> JRJM03Test:
        async with async_db_session() as db:
            row = await jr_jm03_test_dao.get(db, pk)
            if not row:
                raise errors.NotFoundError(msg='数据不存在')
            return row

    @staticmethod
    async def get_select(*, test_snkey: str | None) -> Select:
        return await jr_jm03_test_dao.get_list(test_snkey=test_snkey)

    @staticmethod
    async def create(*, obj: CreateJRJM03TestParam) -> None:
        async with async_db_session.begin() as db:
            await jr_jm03_test_dao.create(db, obj)

    @staticmethod
    async def bulk_create(*, objs: list[CreateJRJM03TestParam]) -> None:
        async with async_db_session.begin() as db:
            await jr_jm03_test_dao.bulk_create(db, objs)

    @staticmethod
    async def delete(*, obj: DeleteJRJM03TestParam) -> int:
        async with async_db_session.begin() as db:
            count = await jr_jm03_test_dao.delete(db, obj.pks)
            return count

    @staticmethod
    async def delete_all() -> None:
        async with async_db_session.begin() as db:
            await jr_jm03_test_dao.delete_all(db)


jr_jm03_test_service: JRJM03TestService = JRJM03TestService()
