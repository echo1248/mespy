# -*- coding: UTF-8 -*-
"""
@Project : jiqid-py
@File    : dy_pallet.py
@Author  : guhua@jiqid.com
@Date    : 2025/08/19 19:07
"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, Integer, CHAR, Index
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import DataClassBase, id_key


class DyPallet(DataClassBase):
    """栈板表"""

    __tablename__ = 'dy_pallet'
    __table_args__ = (
        # 唯一索引（cartonkey唯一）
        Index('pallet_cartonkey_index', 'pallet_cartonkey', unique=True),

        # 复合索引
        Index('test_sn_createdon_index', 'pallet_cartonkey', 'pallet_created_on'),

        # 单列索引
        Index('pallet_created_on_index', 'pallet_created_on'),
        Index('pallet_creator_key_index', 'pallet_creator_key'),
        Index('pallet_date_index', 'pallet_date'),
        Index('pallet_delivered_on_index', 'pallet_delivered_on'),
        Index('pallet_key_index', 'pallet_key'),
        Index('pallet_pid_index', 'pallet_pid'),
        Index('pallet_po_index', 'pallet_po'),
        Index('pallet_sku_index', 'pallet_sku'),
        Index('pallet_spec_index', 'pallet_spec'),
        Index('pallet_title_index', 'pallet_title'),
        Index('pallet_weight_idnex', 'pallet_weight'),

        {'comment': '栈板表'}
    )

    pallet_id: Mapped[id_key] = mapped_column(init=False, comment='主键ID')
    pallet_po: Mapped[str] = mapped_column(CHAR(32), comment='采购订单号')
    pallet_sku: Mapped[str] = mapped_column(CHAR(32), comment='SKU编码')
    pallet_pid: Mapped[str] = mapped_column(CHAR(32), comment='产品ID')
    pallet_date: Mapped[str] = mapped_column(CHAR(32), comment='日期')
    pallet_title: Mapped[str] = mapped_column(String(64), comment='标题')
    pallet_spec: Mapped[str] = mapped_column(String(32), comment='规格')
    pallet_deficient: Mapped[bool] = mapped_column(Boolean, nullable=True, comment='是否缺货')
    pallet_weight: Mapped[str] = mapped_column(String(32), comment='重量')
    pallet_num: Mapped[int] = mapped_column(Integer, nullable=True, comment='当前数量')
    pallet_maxnum: Mapped[int] = mapped_column(Integer, comment='最大数量')  # NOT NULL，需要确保有值
    pallet_key: Mapped[str] = mapped_column(CHAR(32), comment='栈板号(栈板标)')
    pallet_warehouse: Mapped[str | None] = mapped_column(String(32), nullable=True, comment='仓库')
    pallet_cartonkey: Mapped[str] = mapped_column(CHAR(32), comment='箱号(箱标)，关联dy_carton表')
    pallet_created_on: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True,
                                                               comment='创建时间')
    pallet_creator_key: Mapped[str | None] = mapped_column(CHAR(32), nullable=True, comment='创建者编码')
    pallet_deleted: Mapped[bool] = mapped_column(Boolean, comment='是否删除')
    pallet_deleter_code: Mapped[str | None] = mapped_column(CHAR(32), nullable=True, comment='删除者编码')
    pallet_deleted_on: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True,
                                                               comment='删除时间')
    pallet_delivered: Mapped[bool] = mapped_column(Boolean, comment='是否已交付')
    pallet_delivered_on: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True,
                                                                 comment='交付时间')
    pallet_cartonpallet_checked: Mapped[bool] = mapped_column(Boolean, nullable=True,
                                                              comment='纸箱托盘检查状态')
    pallet_printlock: Mapped[bool] = mapped_column(Boolean, comment='打印锁定')
    pallet_printunlock_userkey: Mapped[str | None] = mapped_column(CHAR(32), nullable=True, comment='打印解锁用户编码')
    pallet_printunlocked_on: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True,
                                                                     comment='打印解锁时间')
