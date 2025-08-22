#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select

from backend.app.mes.crud.crud_dy_carton import dy_carton_dao
from backend.app.mes.model import DyCarton
from backend.app.mes.schema.dy_carton import CreateDyCartonParam, DeleteDyCartonParam
from backend.common.exception import errors
from backend.database.db import async_db_session


class DyCartonService:

    @staticmethod
    async def get(*, pk: int) -> DyCarton:
        async with async_db_session() as db:
            row = await dy_carton_dao.get(db, pk)
            if not row:
                raise errors.NotFoundError(msg='数据不存在')
            return row

    @staticmethod
    async def get_select(*, carton_key: str | None) -> Select:
        return await dy_carton_dao.get_list(carton_key=carton_key)

    @staticmethod
    async def create(*, obj: CreateDyCartonParam) -> None:
        async with async_db_session.begin() as db:
            await dy_carton_dao.create(db, obj)

    @staticmethod
    async def bulk_create(*, objs: list[CreateDyCartonParam]) -> None:
        async with async_db_session.begin() as db:
            await dy_carton_dao.bulk_create(db, objs)

    @staticmethod
    async def delete(*, obj: DeleteDyCartonParam) -> int:
        async with async_db_session.begin() as db:
            count = await dy_carton_dao.delete(db, obj.pks)
            return count

    @staticmethod
    async def delete_all() -> None:
        async with async_db_session.begin() as db:
            await dy_carton_dao.delete_all(db)


dy_carton_service: DyCartonService = DyCartonService()
