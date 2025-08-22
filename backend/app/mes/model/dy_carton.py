# -*- coding: UTF-8 -*-
"""
@Project : jiqid-py
@File    : dy_carton.py
@Author  : guhua@jiqid.com
@Date    : 2025/08/19 19:14
"""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, Integer, CHAR, DECIMAL
from sqlalchemy.dialects.postgresql import INTEGER, NUMERIC
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import DataClassBase, id_key


class DyCarton(DataClassBase):
    """纸箱表"""

    __tablename__ = 'dy_carton'

    carton_id: Mapped[id_key] = mapped_column(init=False)
    carton_key: Mapped[str] = mapped_column(CHAR(32), comment='箱号(箱标)')
    carton_sku: Mapped[str] = mapped_column(CHAR(32), comment='SKU编码')
    carton_cartonindex: Mapped[int] = mapped_column(Integer, comment='纸箱索引')
    carton_palletindex: Mapped[int] = mapped_column(Integer, comment='栈板索引')
    carton_prodid: Mapped[str] = mapped_column(
        CHAR(32), comment='产品ID（过渡栏位，最终用carton_sku.sql更新，procGetCarton）'
    )
    carton_boxsn: Mapped[str] = mapped_column(CHAR(64), comment='产品的SN号')
    carton_num: Mapped[int] = mapped_column(Integer, comment='数量')
    carton_weight: Mapped[Decimal] = mapped_column(
        DECIMAL(10, 2).with_variant(NUMERIC(10, 2), 'postgresql'),
        comment='重量'
    )
    carton_weighting_key: Mapped[str] = mapped_column(CHAR(32), comment='称重编码')
    carton_weighting_on: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), comment='称重时间')
    carton_deficient: Mapped[bool] = mapped_column(
        Boolean().with_variant(INTEGER, 'postgresql'), comment='是否满箱'
    )
    carton_created_on: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), comment='创建时间')
    carton_creator_key: Mapped[str] = mapped_column(CHAR(32), comment='创建者编码')
    carton_deleted: Mapped[bool] = mapped_column(
        Boolean().with_variant(INTEGER, 'postgresql'), comment='是否删除'
    )
    carton_deleter_code: Mapped[str] = mapped_column(CHAR(32), comment='删除者编码')
    carton_deleted_on: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), comment='删除时间')
    carton_delivered: Mapped[bool] = mapped_column(
        Boolean().with_variant(INTEGER, 'postgresql'), comment='是否已交付'
    )
    carton_delivered_on: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), comment='交付时间')
    carton_printlock: Mapped[bool] = mapped_column(
        Boolean().with_variant(INTEGER, 'postgresql'), comment='打印锁定'
    )
    carton_printunlock_userkey: Mapped[str] = mapped_column(CHAR(32), comment='打印解锁用户编码')
    carton_printunlocked_on: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), comment='打印解锁时间')
    carton_rma: Mapped[int] = mapped_column(Integer, comment='是否为RMA售后机装错（0否，1是）')
