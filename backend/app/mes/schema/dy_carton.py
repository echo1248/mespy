#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from decimal import Decimal

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class DyCartonSchemaBase(SchemaBase):
    """纸箱基础模型"""

    carton_key: str = Field(description='箱号(箱标)')
    carton_sku: str = Field(description='SKU编码')
    carton_cartonindex: int = Field(description='纸箱索引')
    carton_palletindex: int = Field(description='托盘索引')
    carton_prodid: str = Field(description='产品ID（过渡栏位）')
    carton_boxsn: str = Field(description='箱序列号')
    carton_num: int = Field(description='数量')
    carton_weight: Decimal = Field(description='重量')
    carton_weighting_key: str | None = Field(None, description='称重编码')
    carton_weighting_on: datetime | None = Field(None, description='称重时间')
    carton_deficient: bool = Field(False, description='是否缺货')
    carton_created_on: datetime | None = Field(None, description='创建时间')
    carton_creator_key: str | None = Field(None, description='创建者编码')
    carton_deleted: bool = Field(False, description='是否删除')
    carton_deleter_code: str | None = Field(None, description='删除者编码')
    carton_deleted_on: datetime | None = Field(None, description='删除时间')
    carton_delivered: bool = Field(False, description='是否已交付')
    carton_delivered_on: datetime | None = Field(None, description='交付时间')
    carton_printlock: bool = Field(False, description='打印锁定')
    carton_printunlock_userkey: str | None = Field(None, description='打印解锁用户编码')
    carton_printunlocked_on: datetime | None = Field(None, description='打印解锁时间')
    carton_rma: int = Field(0, description='是否为RMA售后机装错（0否，1是）')


class CreateDyCartonParam(DyCartonSchemaBase):
    """创建纸箱参数"""


class UpdateDyCartonParam(DyCartonSchemaBase):
    """更新纸箱参数"""


class DeleteDyCartonParam(SchemaBase):
    """删除纸箱参数"""

    pks: list[int] = Field(description='纸箱ID列表')


class GetDyCartonDetail(DyCartonSchemaBase):
    """纸箱详情"""

    model_config = ConfigDict(from_attributes=True)

    carton_id: int = Field(description='纸箱ID')
