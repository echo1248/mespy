#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select
from sqlalchemy import delete as sa_delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.mes.model import DyPallet
from backend.app.mes.schema.dy_pallet import CreateDyPalletParam


class CRUDDyPalletDao(CRUDPlus[DyPallet]):

    async def get(self, db: AsyncSession, pk: int) -> DyPallet | None:
        return await self.select_model_by_column(db, id=pk)

    async def get_list(self, pallet_pid: str | None, pallet_key: str | None) -> Select:
        filters = {}
        if pallet_pid is not None:
            filters['pallet_pid__eq'] = pallet_pid
        if pallet_key is not None:
            filters['pallet_key__eq'] = pallet_key
        return await self.select_order('pallet_id', 'desc', **filters)

    async def create(self, db: AsyncSession, obj: CreateDyPalletParam) -> None:
        await self.create_model(db, obj)

    async def bulk_create(self, db: AsyncSession, objs: list[CreateDyPalletParam]) -> None:
        await self.create_models(db, objs)

    async def delete(self, db: AsyncSession, pks: list[int]) -> int:
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pks)

    @staticmethod
    async def delete_all(db: AsyncSession) -> None:
        await db.execute(sa_delete(DyPallet))


dy_pallet_dao: CRUDDyPalletDao = CRUDDyPalletDao(DyPallet)
