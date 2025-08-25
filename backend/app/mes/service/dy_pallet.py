#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from sqlalchemy import Select

from backend.app.mes.crud.crud_dy_carton import dy_carton_dao
from backend.app.mes.crud.crud_dy_pallet import dy_pallet_dao
from backend.app.mes.crud.prod.crud_xm_oh2_test import xm_oh2_test_dao
from backend.app.mes.model import DyPallet
from backend.app.mes.schema.dy_pallet import CreateDyPalletParam, DeleteDyPalletParam, BillParam
from backend.app.mes.schema.prod.xm_oh2_test import CreateXMOH2TestParam
from backend.common.exception import errors
from backend.database.db import async_db_session
from backend.utils.timezone import timezone


class DyPalletService:

    @staticmethod
    async def get(*, pk: int) -> DyPallet:
        async with async_db_session() as db:
            row = await dy_pallet_dao.get(db, pk)
            if not row:
                raise errors.NotFoundError(msg='数据不存在')
            return row

    @staticmethod
    async def get_select(*, pallet_pid: str | None, pallet_key: str | None) -> Select:
        return await dy_pallet_dao.get_list(pallet_pid=pallet_pid, pallet_key=pallet_key)

    @staticmethod
    async def create(*, obj: CreateDyPalletParam) -> None:
        async with async_db_session.begin() as db:
            await dy_pallet_dao.create(db, obj)

    @staticmethod
    async def bulk_create(*, objs: list[CreateDyPalletParam]) -> None:
        async with async_db_session.begin() as db:
            await dy_pallet_dao.bulk_create(db, objs)

    @staticmethod
    async def delete(*, obj: DeleteDyPalletParam) -> int:
        async with async_db_session.begin() as db:
            count = await dy_pallet_dao.delete(db, obj.pks)
            return count

    @staticmethod
    async def delete_all() -> None:
        async with async_db_session.begin() as db:
            await dy_pallet_dao.delete_all(db)

    async def approve_in_bill(self, bill_params: List[BillParam]) -> None:
        await self._approve_bill(bill_params, "in")

    async def approve_out_bill(self, bill_params: List[BillParam]) -> None:
        await self._approve_bill(bill_params, "out")

    async def reverse_in_bill(self, bill_params: List[BillParam]) -> None:
        await self._reverse_bill(bill_params, "in")

    async def reverse_out_bill(self, bill_params: List[BillParam]) -> None:
        await self._reverse_bill(bill_params, "out")

    async def _approve_bill(self, bill_params: List[BillParam], bill_type: str) -> None:
        pallets, cartons = await self.check_bill(bill_params)
        cartonkey_pallet_map = {row.pallet_cartonkey: row for row in pallets}
        bill_map = {row.pallet_pid: row for row in bill_params}

        async with async_db_session.begin() as db:
            objs = []
            for carton in cartons:
                pallet = cartonkey_pallet_map[carton.carton_key]
                bill = bill_map[pallet.pallet_pid]
                objs.append(CreateXMOH2TestParam(
                    test_snkey=carton.carton_boxsn,
                    test_stkey="ASSY_IS" if bill_type == "in" else "ASSY_OS",
                    test_sttitle="成品入库" if bill_type == "in" else "成品出库",
                    test_times_putin=1,
                    test_pid=pallet.pallet_pid,
                    test_skukey=pallet.pallet_key,
                    test_skutitle=pallet.pallet_title,
                    test_pass_1=1,
                    test_info_1="金蝶入库",
                    test_createdon=timezone.now(),
                    test_orderkey_s=bill.orderkey_s,
                    test_orderkey=bill.orderkey,
                ))

            await xm_oh2_test_dao.bulk_create(db, objs)

    async def _reverse_bill(self, bill_params: List[BillParam], bill_type: str):
        _, cartons = await self.check_bill(bill_params)
        snkeys = [carton.carton_boxsn for carton in cartons]

        async with async_db_session.begin() as db:
            await xm_oh2_test_dao.delete_model_by_column(db, allow_multiple=True, test_snkey__in=snkeys)

    @staticmethod
    async def check_bill(bill_params: List[BillParam]):
        """ 参数校验 """
        async with async_db_session() as db:
            pallets = []
            for item in bill_params:
                if item.pallet_pid not in ("61346",):
                    raise errors.ForbiddenError(msg=f'参数错误[pallet_pid={item.pallet_pid}]')

                rows = await dy_pallet_dao.select_models(db, pallet_key__eq=item.pallet_key)
                if not rows:
                    raise errors.NotFoundError(msg=f'栈板号不存在[pallet_key={item.pallet_key}]')

                rows = [row for row in rows if row.pallet_pid == item.pallet_pid]
                if not rows:
                    raise errors.NotFoundError(
                        msg=f'数据不存在[pallet_key={item.pallet_key}, pallet_pid={item.pallet_pid}]')

                pallets.extend(rows)

            carton_keys = [row.pallet_cartonkey for row in pallets]
            cartons = await dy_carton_dao.select_models(db, carton_key__in=carton_keys)

            return pallets, cartons


dy_pallet_service: DyPalletService = DyPalletService()
