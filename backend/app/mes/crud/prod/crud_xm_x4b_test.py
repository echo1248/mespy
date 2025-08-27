#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select
from sqlalchemy import delete as sa_delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.mes.model import XMX4BTest
from backend.app.mes.schema.prod.xm_x4b_test import CreateXMX4BTestParam


class CRUDXMX4BTestDao(CRUDPlus[XMX4BTest]):

    async def get(self, db: AsyncSession, pk: int) -> XMX4BTest | None:
        return await self.select_model_by_column(db, id=pk)

    async def get_list(self, test_snkey: str | None) -> Select:
        filters = {}
        if test_snkey is not None:
            filters['test_snkey__eq'] = test_snkey
        return await self.select_order('test_id', 'desc', **filters)

    async def create(self, db: AsyncSession, obj: CreateXMX4BTestParam) -> None:
        await self.create_model(db, obj)

    async def bulk_create(self, db: AsyncSession, objs: list[CreateXMX4BTestParam]) -> None:
        await self.create_models(db, objs)

    async def delete(self, db: AsyncSession, pks: list[int]) -> int:
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pks)

    @staticmethod
    async def delete_all(db: AsyncSession) -> None:
        await db.execute(sa_delete(XMX4BTest))


xm_x4b_test_dao: CRUDXMX4BTestDao = CRUDXMX4BTestDao(XMX4BTest)
