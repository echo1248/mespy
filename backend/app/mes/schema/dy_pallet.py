#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class DyPalletSchemaBase(SchemaBase):
    """栈板基础模型"""

    pallet_po: str = Field(description='采购订单号')
    pallet_sku: str = Field(description='SKU编码')
    pallet_pid: str = Field(description='产品ID')
    pallet_date: str = Field(description='日期')
    pallet_title: str = Field(description='标题')
    pallet_spec: str = Field(description='规格')
    pallet_deficient: bool = Field(False, description='是否缺货')
    pallet_weight: str = Field(description='重量')
    pallet_num: int = Field(description='当前数量')
    pallet_maxnum: int = Field(description='最大数量')
    pallet_key: str = Field(description='栈板号(栈板标)')
    pallet_warehouse: str = Field(description='仓库')
    pallet_cartonkey: str = Field(description='箱号(箱标)')
    pallet_created_on: datetime | None = Field(None, description='创建时间')
    pallet_creator_key: str | None = Field(None, description='创建者编码')
    pallet_deleted: bool = Field(False, description='是否删除')
    pallet_deleter_code: str | None = Field(None, description='删除者编码')
    pallet_deleted_on: datetime | None = Field(None, description='删除时间')
    pallet_delivered: bool = Field(False, description='是否已交付')
    pallet_delivered_on: datetime | None = Field(None, description='交付时间')
    pallet_cartonpallet_checked: bool = Field(False, description='纸箱托盘检查状态')
    pallet_printlock: str | None = Field(None, description='打印锁定')
    pallet_printunlock_userkey: str | None = Field(None, description='打印解锁用户编码')
    pallet_printunlocked_on: datetime | None = Field(None, description='打印解锁时间')


class CreateDyPalletParam(DyPalletSchemaBase):
    """创建托盘参数"""


class UpdateDyPalletParam(DyPalletSchemaBase):
    """更新托盘参数"""


class DeleteDyPalletParam(SchemaBase):
    """删除托盘参数"""

    pks: list[int] = Field(description='托盘ID列表')


class GetDyPalletDetail(DyPalletSchemaBase):
    """托盘详情"""

    model_config = ConfigDict(from_attributes=True)

    pallet_id: int = Field(description='托盘ID')


class BillParam(SchemaBase):
    """审核单据参数"""
    pallet_pid: str = Field(description='产品ID')
    pallet_key: str = Field(description='栈板号(栈板标)')
    orderkey_s: str = Field(description='订单号(溯源)')
    orderkey: str = Field(description='订单号')


class BillParamList(SchemaBase):
    """审核单据参数"""
    items: list[BillParam] = Field(description='审核参数列表')
