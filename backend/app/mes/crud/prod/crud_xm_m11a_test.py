#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select
from sqlalchemy import delete as sa_delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.mes.model import XMM11ATest
from backend.app.mes.schema.prod.xm_m11a_test import CreateXMM11ATestParam


class CRUDXMM11ATestDao(CRUDPlus[XMM11ATest]):

    async def get(self, db: AsyncSession, pk: int) -> XMM11ATest | None:
        return await self.select_model_by_column(db, id=pk)

    async def get_list(self, test_snkey: str | None) -> Select:
        filters = {}
        if test_snkey is not None:
            filters['test_snkey__eq'] = test_snkey
        return await self.select_order('test_id', 'desc', **filters)

    async def create(self, db: AsyncSession, obj: CreateXMM11ATestParam) -> None:
        await self.create_model(db, obj)

    async def bulk_create(self, db: AsyncSession, objs: list[CreateXMM11ATestParam]) -> None:
        await self.create_models(db, objs)

    async def delete(self, db: AsyncSession, pks: list[int]) -> int:
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pks)

    @staticmethod
    async def delete_all(db: AsyncSession) -> None:
        await db.execute(sa_delete(XMM11ATest))


xm_m11a_test_dao: CRUDXMM11ATestDao = CRUDXMM11ATestDao(XMM11ATest)
