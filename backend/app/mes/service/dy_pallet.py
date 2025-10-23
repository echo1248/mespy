#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from typing import List, Sequence
from dataclasses import dataclass

from sqlalchemy import Select, insert

from backend.app.mes.crud.crud_dy_carton import dy_carton_dao
from backend.app.mes.crud.crud_dy_pallet import dy_pallet_dao
from backend.app.mes.crud.prod.crud_dy_qbh4248cn_test import dy_qbh4248cn_test_dao
from backend.app.mes.crud.prod.crud_jr_jm03_test import jr_jm03_test_dao
from backend.app.mes.crud.prod.crud_xm_l0b5_test import xm_l05b_test_dao
from backend.app.mes.crud.prod.crud_xm_m11a_test import xm_m11a_test_dao
from backend.app.mes.crud.prod.crud_xm_oh11_test import xm_oh11_test_dao
from backend.app.mes.crud.prod.crud_xm_oh2_test import xm_oh2_test_dao
from backend.app.mes.crud.prod.crud_xm_oh3r_test import xm_oh3r_test_dao
from backend.app.mes.crud.prod.crud_xm_x4b_test import xm_x4b_test_dao
from backend.app.mes.crud.prod.crud_xm_x6a_test import xm_x6a_test_dao
from backend.app.mes.crud.prod.crud_xm_x8c_test import xm_x8c_test_dao
from backend.app.mes.crud.prod.crud_xm_x8f_test import xm_x8f_test_dao
from backend.app.mes.crud.prod.crud_xm_xhb_test import xm_xhb_test_dao
from backend.app.mes.crud.prod.crud_yz_mc601_test import yz_mc601_test_dao
from backend.app.mes.crud.prod.crud_yz_mc60_01_test import yz_mc60_01_test_dao
from backend.app.mes.model import DyPallet, DyCarton
from backend.app.mes.schema.dy_pallet import CreateDyPalletParam, DeleteDyPalletParam, BillParam
from backend.app.mes.schema.prod.dy_qbh4248cn_test import CreateDyQBH4248CNTestParam
from backend.app.mes.schema.prod.jr_jm03_test import CreateJRJM03TestParam
from backend.app.mes.schema.prod.xm_l05b_test import CreateXML05BTestParam
from backend.app.mes.schema.prod.xm_m11a_test import CreateXMM11ATestParam
from backend.app.mes.schema.prod.xm_oh11_test import CreateXMOH11TestParam
from backend.app.mes.schema.prod.xm_oh2_test import CreateXMOH2TestParam
from backend.app.mes.schema.prod.xm_oh3r_test import CreateXMOH3RTestParam
from backend.app.mes.schema.prod.xm_x4b_test import CreateXMX4BTestParam
from backend.app.mes.schema.prod.xm_x6a_test import CreateXMX6ATestParam
from backend.app.mes.schema.prod.xm_x8c_test import CreateXMX8CTestParam
from backend.app.mes.schema.prod.xm_x8f_test import CreateXMX8FTestParam
from backend.app.mes.schema.prod.xm_xhb_test import CreateXMXHBTestParam
from backend.app.mes.schema.prod.yz_mc601_test import CreateYZMC601TestParam
from backend.app.mes.schema.prod.yz_mc60_01_test import CreateYZMC6001TestParam
from backend.common.exception import errors
from backend.common.log import log
from backend.database.db import async_db_session
from backend.utils.timezone import timezone


@dataclass
class BillOperationConfig:
    """单据操作配置"""
    test_stkey: str
    test_sttitle: str
    test_info_1: str


class DyPalletService:
    # 常量配置
    BILL_CONFIGS = {
        "in": BillOperationConfig("ASSY_IS", "成品入库", "金蝶入库"),
        "out": BillOperationConfig("ASSY_OS", "成品出库", "金蝶出库")
    }

    # 产品映射配置
    PID_MAP = {
        # JM03
        "933006": jr_jm03_test_dao, "933007": jr_jm03_test_dao,
        "933002": jr_jm03_test_dao, "933008": jr_jm03_test_dao,

        # L05B/C
        "31833": xm_l05b_test_dao, "31834": xm_l05b_test_dao,

        # M11A
        "57470": xm_m11a_test_dao, "58472": xm_m11a_test_dao, "58473": xm_m11a_test_dao,

        # OH2
        "61346": xm_oh2_test_dao, "73528": xm_oh2_test_dao, "73529": xm_oh2_test_dao,
        "73530": xm_oh2_test_dao, "73531": xm_oh2_test_dao, "73532": xm_oh2_test_dao,

        # OH3R
        "66522": xm_oh3r_test_dao, "66523": xm_oh3r_test_dao, "70163": xm_oh3r_test_dao,
        "66524": xm_oh3r_test_dao, "66525": xm_oh3r_test_dao,

        # OH11
        "66286": xm_oh11_test_dao, "73648": xm_oh11_test_dao,

        # X4B
        "55119": xm_x4b_test_dao, "69675": xm_x4b_test_dao,

        # X6A
        "41052": xm_x6a_test_dao,

        # X8C
        "27414": xm_x8c_test_dao,

        # X8F
        "48350": xm_x8f_test_dao,

        # MC60-01
        "60314": yz_mc60_01_test_dao,

        # MC601
        "60317": yz_mc601_test_dao, "63605": yz_mc601_test_dao,

        # QBH
        "44481": dy_qbh4248cn_test_dao,

        # XHB
        "47303": xm_xhb_test_dao, "44573": xm_xhb_test_dao, "44574": xm_xhb_test_dao, "28505": xm_xhb_test_dao,
    }

    # 参数类型映射
    CREATE_PARAM_MAP = {
        jr_jm03_test_dao: CreateJRJM03TestParam,
        xm_l05b_test_dao: CreateXML05BTestParam,
        xm_m11a_test_dao: CreateXMM11ATestParam,
        xm_oh2_test_dao: CreateXMOH2TestParam,
        xm_oh3r_test_dao: CreateXMOH3RTestParam,
        xm_oh11_test_dao: CreateXMOH11TestParam,
        xm_x4b_test_dao: CreateXMX4BTestParam,
        xm_x6a_test_dao: CreateXMX6ATestParam,
        xm_x8c_test_dao: CreateXMX8CTestParam,
        xm_x8f_test_dao: CreateXMX8FTestParam,
        yz_mc60_01_test_dao: CreateYZMC6001TestParam,
        yz_mc601_test_dao: CreateYZMC601TestParam,
        dy_qbh4248cn_test_dao: CreateDyQBH4248CNTestParam,
        xm_xhb_test_dao: CreateXMXHBTestParam,
    }

    @staticmethod
    async def get(*, pk: int) -> DyPallet:
        """根据主键获取栈板信息"""
        async with async_db_session() as db:
            row = await dy_pallet_dao.get(db, pk)
            if not row:
                raise errors.NotFoundError(msg='数据不存在')
            return row

    @staticmethod
    async def get_select(*, pallet_pid: str | None = None, pallet_key: str | None = None) -> Select:
        """获取查询语句"""
        return await dy_pallet_dao.get_list(pallet_pid=pallet_pid, pallet_key=pallet_key)

    @staticmethod
    async def create(*, obj: CreateDyPalletParam) -> None:
        """创建栈板"""
        async with async_db_session.begin() as db:
            await dy_pallet_dao.create(db, obj)

    @staticmethod
    async def bulk_create(*, objs: List[CreateDyPalletParam]) -> None:
        """批量创建栈板"""
        async with async_db_session.begin() as db:
            await dy_pallet_dao.bulk_create(db, objs)

    @staticmethod
    async def delete(*, obj: DeleteDyPalletParam) -> int:
        """删除栈板"""
        async with async_db_session.begin() as db:
            count = await dy_pallet_dao.delete(db, obj.pks)
            return count

    @staticmethod
    async def delete_all() -> None:
        """删除所有栈板"""
        async with async_db_session.begin() as db:
            await dy_pallet_dao.delete_all(db)

    async def approve_in_bill(self, bill_params: List[BillParam]) -> None:
        """审核入库单据"""
        return await self._process_bill(bill_params, "in", is_reverse=False)

    async def approve_out_bill(self, bill_params: List[BillParam]) -> None:
        """审核出库单据"""
        return await self._process_bill(bill_params, "out", is_reverse=False)

    async def reverse_in_bill(self, bill_params: List[BillParam]) -> None:
        """撤销入库单据"""
        return await self._process_bill(bill_params, "in", is_reverse=True)

    async def reverse_out_bill(self, bill_params: List[BillParam]) -> None:
        """撤销出库单据"""
        return await self._process_bill(bill_params, "out", is_reverse=True)

    async def _process_bill(self, bill_params: List[BillParam], bill_type: str, is_reverse: bool) -> None:
        """处理单据的核心方法"""
        pallets, cartons = await self._validate_bill_params(bill_params)

        if is_reverse:
            await self._reverse_bill_operation(cartons, bill_params, bill_type)
        else:
            await self._approve_bill_operation(pallets, cartons, bill_params, bill_type)

    async def _approve_bill_operation(self, pallets: List[DyPallet], cartons: Sequence[DyCarton],
                                      bill_params: List[BillParam], bill_type: str) -> None:
        """执行审核单据操作"""
        config = self.BILL_CONFIGS[bill_type]
        pallet_map = {pallet.pallet_cartonkey: pallet for pallet in pallets}
        bill_map = {bill.pallet_pid: bill for bill in bill_params}

        create_objs = []
        for carton in cartons:
            pallet = pallet_map.get(carton.carton_key)
            if pallet is None:
                continue

            bill = bill_map.get(pallet.pallet_pid)
            if bill is None:
                continue

            common_params = {
                "test_sttitle": config.test_sttitle,
                "test_times_putin": 1,
                "test_pid": pallet.pallet_pid,
                "test_skukey": pallet.pallet_key,
                "test_skutitle": pallet.pallet_title,
                "test_pass_on1": timezone.now(),
                "test_pass_testedby1": "MES",
                "test_info_1": config.test_info_1,
                "test_createdon": timezone.now(),
                "test_k3orderkey_s": bill.k3orderkey_s,
                "test_k3orderkey": bill.k3orderkey,
            }

            if pallet.pallet_pid == "44481":  # 音箱
                params = {
                    **common_params,
                    "test_sn": carton.carton_boxsn,
                    "test_funccode": config.test_stkey,
                    "test_result": 0,
                }
            else:
                params = {
                    **common_params,
                    "test_snkey": carton.carton_boxsn,
                    "test_stkey": config.test_stkey,
                    "test_pass_1": 1,
                }

            create_objs.append(params)

        if not create_objs:
            raise errors.NotFoundError(msg="未找到对应的栈板和箱信息")

        for param in bill_params:  # 遍历单据参数，获取对应的产品DAO和参数类
            prod_dao = self.PID_MAP[param.pallet_pid]
            param_class = self.CREATE_PARAM_MAP[prod_dao]
            instances = [param_class(**obj) for obj in create_objs if obj["test_skukey"] == param.pallet_key]
            if not instances:
                log.warning(f"未找到对应的栈板和箱信息: {param}")
                continue

            async with async_db_session.begin() as db:
                data_dicts = [instance.__dict__ for instance in instances]
                await db.execute(prod_dao.model.__table__.insert(), data_dicts)  # noqa 优化批量插入

    async def _reverse_bill_operation(self, cartons: Sequence[DyCarton], bill_params: List[BillParam],
                                      bill_type: str) -> None:
        """执行冲销单据操作"""
        config = self.BILL_CONFIGS[bill_type]
        sn_keys = [carton.carton_boxsn for carton in cartons]

        async with async_db_session.begin() as db:
            for pallet_pid in {param.pallet_pid for param in bill_params}:
                prod_dao = self.PID_MAP[pallet_pid]

                if pallet_pid == "44481":  # 音箱特殊处理
                    await self._handle_speaker_reverse(prod_dao, db, config, sn_keys)
                else:
                    await self._handle_products_reverse(prod_dao, db, config, sn_keys)

    async def _handle_speaker_reverse(self, prod_dao, db, config, sn_keys):
        """处理音箱冲销逻辑"""
        if config.test_stkey == "ASSY_IS":
            count = await prod_dao.count(db, test_sn__in=sn_keys, test_funccode="ASSY_OS")
            if count > 0:
                raise errors.RequestError(msg="有已完成出库的栈板，不允许入库反审核")

        await prod_dao.delete_model_by_column(
            db, allow_multiple=True, test_sn__in=sn_keys, test_funccode=config.test_stkey
        )

    async def _handle_products_reverse(self, prod_dao, db, config, sn_keys):
        """处理其他产品冲销逻辑"""
        if config.test_stkey == "ASSY_IS":
            count = await prod_dao.count(db, test_snkey__in=sn_keys, test_stkey="ASSY_OS")
            if count > 0:
                raise errors.RequestError(msg="有已完成出库的栈板，不允许入库反审核")

        await prod_dao.delete_model_by_column(
            db, allow_multiple=True, test_snkey__in=sn_keys, test_stkey=config.test_stkey
        )

    async def _validate_bill_params(self, bill_params: List[BillParam]) -> tuple[List[DyPallet], Sequence]:
        """验证单据参数并获取相关数据"""
        if not bill_params:
            raise errors.RequestError(msg="单据参数不能为空")

        # 验证产品ID支持性
        for item in bill_params:
            if item.pallet_pid not in self.PID_MAP:
                raise errors.RequestError(msg=f'不支持的产品ID: {item.pallet_pid}')

        # 检查重复参数
        self._check_duplicates(bill_params)

        async with async_db_session() as db:
            pallet_keys = [item.pallet_key for item in bill_params]
            all_pallets = await dy_pallet_dao.select_models(db, pallet_key__in=pallet_keys)

            error_list = []
            valid_pallets = []
            for param in bill_params:
                matching_pallets = [
                    p for p in all_pallets
                    if p.pallet_key == param.pallet_key and p.pallet_pid == param.pallet_pid
                ]
                if not matching_pallets:
                    error_list.append({"msg": "PID不存在或栈板号不存在", **param.model_dump()})
                    continue

                valid_pallets.extend(matching_pallets)
                error_list.append({"msg": None, **param.model_dump()})

            # 如果有错误立即返回，避免不必要的数据库查询
            if error_list and any(item["msg"] for item in error_list):
                raise errors.RequestError(msg=json.dumps(error_list))

            # 批量查询箱信息
            carton_keys = [pallet.pallet_cartonkey for pallet in valid_pallets]
            cartons = await dy_carton_dao.select_models(
                db, carton_key__in=carton_keys
            ) if carton_keys else []

            return valid_pallets, cartons

    def _check_duplicates(self, bill_params: List[BillParam]) -> None:
        """快速检查是否存在重复参数"""
        pallet_keys = set()

        for param in bill_params:
            if not param.pallet_key:
                raise errors.RequestError(msg=f"栈板号为空")

            if param.pallet_key in pallet_keys:
                raise errors.RequestError(msg=f"存在重复的栈板号: {param.pallet_key}")
            pallet_keys.add(param.pallet_key)

    @classmethod
    def get_supported_pids(cls) -> List[str]:
        """获取支持的产品ID列表"""
        return list(cls.PID_MAP.keys())


# 服务实例
dy_pallet_service = DyPalletService()
