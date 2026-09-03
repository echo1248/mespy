#!/usr/bin/env python3
from sqlalchemy import Select
from sqlalchemy import delete as sa_delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.mes.model import XMQH2PTest
from backend.app.mes.schema.prod.xm_qh2p_test import CreateXMQH2PTestParam


class CRUDXMQH2PTestDao(CRUDPlus[XMQH2PTest]):
    async def get(self, db: AsyncSession, pk: int) -> XMQH2PTest | None:
        return await self.select_model(db, pk)

    async def get_list(self, test_snkey: str | None) -> Select:
        filters = {}
        if test_snkey is not None:
            filters['test_snkey__eq'] = test_snkey
        return await self.select_order('test_id', 'desc', **filters)

    async def create(self, db: AsyncSession, obj: CreateXMQH2PTestParam) -> None:
        await self.create_model(db, obj)

    async def bulk_create(self, db: AsyncSession, objs: list[CreateXMQH2PTestParam]) -> None:
        await self.create_models(db, objs)

    async def delete(self, db: AsyncSession, pks: list[int]) -> int:
        return await self.delete_model_by_column(db, allow_multiple=True, test_id__in=pks)

    @staticmethod
    async def delete_all(db: AsyncSession) -> None:
        await db.execute(sa_delete(XMQH2PTest))


xm_qh2p_test_dao: CRUDXMQH2PTestDao = CRUDXMQH2PTestDao(XMQH2PTest)
