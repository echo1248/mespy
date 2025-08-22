#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select
from sqlalchemy import delete as sa_delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.mes.model import DyCarton
from backend.app.mes.schema.dy_carton import CreateDyCartonParam


class CRUDDyCartonDao(CRUDPlus[DyCarton]):

    async def get(self, db: AsyncSession, pk: int) -> DyCarton | None:
        return await self.select_model_by_column(db, id=pk)

    async def get_list(self, carton_key: str | None) -> Select:
        filters = {}
        if carton_key is not None:
            filters['carton_key__eq'] = carton_key
        return await self.select_order('carton_id', 'desc', **filters)

    async def create(self, db: AsyncSession, obj: CreateDyCartonParam) -> None:
        await self.create_model(db, obj)

    async def bulk_create(self, db: AsyncSession, objs: list[CreateDyCartonParam]) -> None:
        await self.create_models(db, objs)

    async def delete(self, db: AsyncSession, pks: list[int]) -> int:
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pks)

    @staticmethod
    async def delete_all(db: AsyncSession) -> None:
        await db.execute(sa_delete(DyCarton))


dy_carton_dao: CRUDDyCartonDao = CRUDDyCartonDao(DyCarton)
