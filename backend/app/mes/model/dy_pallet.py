# -*- coding: UTF-8 -*-
"""
@Project : jiqid-py
@File    : dy_pallet.py
@Author  : guhua@jiqid.com
@Date    : 2025/08/19 19:07
"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, Integer, CHAR
from sqlalchemy.dialects.postgresql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import DataClassBase, id_key


class DyPallet(DataClassBase):
    """栈板表"""

    __tablename__ = 'dy_pallet'

    pallet_id: Mapped[id_key] = mapped_column(init=False)
    pallet_po: Mapped[str] = mapped_column(CHAR(32), comment='采购订单号')
    pallet_sku: Mapped[str] = mapped_column(CHAR(32), comment='SKU编码')
    pallet_pid: Mapped[str] = mapped_column(CHAR(32), comment='产品ID')
    pallet_date: Mapped[str] = mapped_column(CHAR(32), comment='日期')
    pallet_title: Mapped[str] = mapped_column(String(64), comment='标题')
    pallet_spec: Mapped[str] = mapped_column(String(32), comment='规格')
    pallet_deficient: Mapped[bool] = mapped_column(
        Boolean().with_variant(INTEGER, 'postgresql'), comment='是否缺货'
    )
    pallet_weight: Mapped[str] = mapped_column(String(32), comment='重量')
    pallet_num: Mapped[int] = mapped_column(Integer, comment='当前数量')
    pallet_maxnum: Mapped[int] = mapped_column(Integer, comment='最大数量')
    pallet_key: Mapped[str] = mapped_column(CHAR(32), comment='栈板号(栈板标)')
    pallet_warehouse: Mapped[str] = mapped_column(String(32), comment='仓库')
    pallet_cartonkey: Mapped[str] = mapped_column(CHAR(32), comment='箱号(箱标)，关联dy_carton表')
    pallet_created_on: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), comment='创建时间')
    pallet_creator_key: Mapped[str] = mapped_column(CHAR(32), comment='创建者编码')
    pallet_deleted: Mapped[bool] = mapped_column(
        Boolean().with_variant(INTEGER, 'postgresql'), comment='是否删除'
    )
    pallet_deleter_code: Mapped[str] = mapped_column(CHAR(32), comment='删除者编码')
    pallet_deleted_on: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), comment='删除时间')
    pallet_delivered: Mapped[bool] = mapped_column(
        Boolean().with_variant(INTEGER, 'postgresql'), comment='是否已交付'
    )
    pallet_delivered_on: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), comment='交付时间')
    pallet_cartonpallet_checked: Mapped[bool] = mapped_column(
        Boolean().with_variant(INTEGER, 'postgresql'), comment='纸箱托盘检查状态'
    )
    pallet_printlock: Mapped[str] = mapped_column(CHAR(32), comment='打印锁定')
    pallet_printunlock_userkey: Mapped[str] = mapped_column(CHAR(32), comment='打印解锁用户编码')
    pallet_printunlocked_on: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), comment='打印解锁时间')
