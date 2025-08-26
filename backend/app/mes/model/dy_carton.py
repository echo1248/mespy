# -*- coding: UTF-8 -*-
"""
@Project : jiqid-py
@File    : dy_carton.py
@Author  : guhua@jiqid.com
@Date    : 2025/08/19 19:14
"""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, Integer, CHAR, DECIMAL, Index
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import DataClassBase, id_key


class DyCarton(DataClassBase):
    """纸箱表"""

    __tablename__ = 'dy_carton'
    __table_args__ = (
        # 唯一复合索引（boxsn + rma 组合唯一）
        Index('carton_boxsn_ram', 'carton_boxsn', 'carton_rma', unique=True),

        # 复合索引（boxsn + created_on 组合查询）
        Index('test_sn_createdon_index', 'carton_boxsn', 'carton_created_on'),

        # 单列索引
        Index('carton_boxsn_index', 'carton_boxsn'),
        Index('carton_created_on_index', 'carton_created_on'),
        Index('carton_creator_key_idex', 'carton_creator_key'),
        Index('carton_delivered_on_index', 'carton_delivered_on'),
        Index('carton_key_index', 'carton_key'),

        {'comment': '纸箱管理表'}
    )

    carton_id: Mapped[id_key] = mapped_column(init=False)
    carton_key: Mapped[str] = mapped_column(CHAR(32), comment='箱号(箱标)')
    carton_sku: Mapped[str] = mapped_column(CHAR(32), comment='SKU编码')
    carton_cartonindex: Mapped[int] = mapped_column(Integer, comment='纸箱索引')
    carton_palletindex: Mapped[int] = mapped_column(Integer, comment='栈板索引')
    carton_prodid: Mapped[str] = mapped_column(CHAR(32), comment='产品ID')
    carton_boxsn: Mapped[str] = mapped_column(CHAR(64), comment='产品的SN号')
    carton_num: Mapped[int] = mapped_column(Integer, comment='数量')
    carton_weight: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), comment='重量')
    carton_weighting_key: Mapped[str | None] = mapped_column(CHAR(32), nullable=True, comment='称重编码')
    carton_weighting_on: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True,
                                                                 comment='称重时间')
    carton_deficient: Mapped[bool] = mapped_column(Boolean, comment='是否满箱')
    carton_created_on: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True,
                                                               comment='创建时间')
    carton_creator_key: Mapped[str | None] = mapped_column(CHAR(32), nullable=True, comment='创建者编码')
    carton_deleted: Mapped[bool] = mapped_column(Boolean, comment='是否删除')
    carton_deleter_code: Mapped[str | None] = mapped_column(CHAR(32), nullable=True, comment='删除者编码')
    carton_deleted_on: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True,
                                                               comment='删除时间')
    carton_delivered: Mapped[bool] = mapped_column(Boolean, comment='是否已交付')
    carton_delivered_on: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True,
                                                                 comment='交付时间')
    carton_printlock: Mapped[bool] = mapped_column(Boolean, comment='打印锁定')
    carton_printunlock_userkey: Mapped[str | None] = mapped_column(CHAR(32), nullable=True, comment='打印解锁用户编码')
    carton_printunlocked_on: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True,
                                                                     comment='打印解锁时间')
    carton_rma: Mapped[int] = mapped_column(Integer, default=0, comment='是否为RMA售后机装箱')
