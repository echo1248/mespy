#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select
from sqlalchemy import delete as sa_delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.mes.model import DyQBH4248CNTest
from backend.app.mes.schema.prod.dy_qbh4248cn_test import CreateDyQBH4248CNTestParam


class CRUDDyQBH4248CNTestDao(CRUDPlus[DyQBH4248CNTest]):

    async def get(self, db: AsyncSession, pk: int) -> DyQBH4248CNTest | None:
        return await self.select_model_by_column(db, id=pk)

    async def get_list(self, test_sn: str | None) -> Select:
        filters = {}
        if test_sn is not None:
            filters['test_sn__eq'] = test_sn
        return await self.select_order('test_id', 'desc', **filters)

    async def create(self, db: AsyncSession, obj: CreateDyQBH4248CNTestParam) -> None:
        await self.create_model(db, obj)

    async def bulk_create(self, db: AsyncSession, objs: list[CreateDyQBH4248CNTestParam]) -> None:
        await self.create_models(db, objs)

    async def delete(self, db: AsyncSession, pks: list[int]) -> int:
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pks)

    @staticmethod
    async def delete_all(db: AsyncSession) -> None:
        await db.execute(sa_delete(DyQBH4248CNTest))


dy_qbh4248cn_test_dao: CRUDDyQBH4248CNTestDao = CRUDDyQBH4248CNTestDao(DyQBH4248CNTest)
