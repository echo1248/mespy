# -*- coding: UTF-8 -*-
"""
@Project : mespy
@File    : yz_mc60_01_test.py
@Author  : guhua@jiqid.com
@Date    : 2025/08/26 14:33
"""

from datetime import datetime
from decimal import Decimal
from sqlalchemy import Boolean, DateTime, Integer, CHAR, VARCHAR, TEXT, TIMESTAMP, Index, INTEGER, DECIMAL
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import DataClassBase, id_key


class YZMC6001Test(DataClassBase):
    """yz_mc60_01产品表"""

    __tablename__ = 'yz_mc60_01_test'

    __table_args__ = (
        # 唯一索引
        Index('test_stkey_snkey_index', 'test_stkey', 'test_snkey', 'test_times_putin', unique=True),

        # 普通索引
        Index('test_stkey_index', 'test_stkey'),
        Index('test_snkey_index', 'test_snkey'),
        Index('test_subkey_idnex', 'test_subkey'),
        Index('test_wifimac_index', 'test_wifimac'),
        Index('test_btmac_index', 'test_btmac'),
        Index('test_did_index', 'test_did'),
        Index('test_key_index', 'test_key'),
        Index('test_stkey_subkey_index', 'test_stkey', 'test_subkey', 'test_times_putin'),
        Index('test_pid_index', 'test_pid'),
        Index('test_skukey_index', 'test_skukey'),
        Index('test_skutitle_index', 'test_skutitle'),
        Index('test_sttitle_index', 'test_sttitle'),
        Index('test_createdon_index', 'test_createdon'),
        Index('test_sn_createdon_index', 'test_createdon', 'test_snkey'),

        # 表注释
        {'comment': 'yz_mc60_01产品表'}
    )

    test_id: Mapped[id_key] = mapped_column(init=False, comment='主键ID')
    test_pid: Mapped[str | None] = mapped_column(CHAR(32), comment='产品ID')
    test_skukey: Mapped[str | None] = mapped_column(CHAR(32), comment='SKU键')
    test_skutitle: Mapped[str | None] = mapped_column(VARCHAR(128), comment='SKU标题')
    test_expired: Mapped[bool] = mapped_column(  # 新增字段
        Boolean().with_variant(INTEGER, 'postgresql'),
        comment='子件重投后，之前轮次的测试信息过期，置为1'
    )
    test_deleted: Mapped[bool] = mapped_column(
        Boolean().with_variant(INTEGER, 'postgresql'),
        comment='是否删除: 0-未删除, 1-已删除'
    )
    test_createdon: Mapped[datetime | None] = mapped_column(
        TIMESTAMP,
        comment='创建时间'
    )
    test_stkey: Mapped[str] = mapped_column(CHAR(32), comment='测试站键')
    test_sttitle: Mapped[str | None] = mapped_column(VARCHAR(32), comment='测试站标题')
    test_stord: Mapped[int | None] = mapped_column(Integer, comment='测试站顺序')
    test_snkey: Mapped[str | None] = mapped_column(CHAR(32), comment='序列号键')
    test_times_putin: Mapped[int] = mapped_column(
        Integer,
        comment='同一个SN，初轮及维修后投入产线轮数'  # 修正注释
    )
    test_pass_1: Mapped[int] = mapped_column(
        Integer().with_variant(TINYINT(1), 'mysql'),
        comment='同一轮投入的第1次测试：0,测试失败，1测试通过，2未测试状态'
    )
    test_pass_2: Mapped[int] = mapped_column(
        Integer().with_variant(TINYINT(1), 'mysql'),
        comment='同一轮投入的第2次测试：0,测试失败，1测试通过，2未测试状态'
    )
    test_pass_3: Mapped[int] = mapped_column(
        Integer().with_variant(TINYINT(1), 'mysql'),
        comment='同一轮投入的第3次测试：0,测试失败，1测试通过，2未测试状态'
    )
    test_info_1: Mapped[str | None] = mapped_column(TEXT, comment='测试信息1')
    test_info_2: Mapped[str | None] = mapped_column(TEXT, comment='测试信息2')
    test_info_3: Mapped[str | None] = mapped_column(TEXT, comment='测试信息3')
    test_subkey: Mapped[str | None] = mapped_column(CHAR(64), comment='绑定的子件物料')
    test_wifimac: Mapped[str | None] = mapped_column(CHAR(32), comment='WIFI MAC地址')
    test_btmac: Mapped[str | None] = mapped_column(CHAR(32), comment='蓝牙MAC地址')
    test_did: Mapped[str | None] = mapped_column(CHAR(32), comment='设备ID')
    test_key: Mapped[str | None] = mapped_column(CHAR(32), comment='测试键')
    test_info: Mapped[str | None] = mapped_column(TEXT, comment='测试信息')
    test_infoecho: Mapped[str | None] = mapped_column(TEXT, comment='测试信息回显')
    test_failkey: Mapped[str | None] = mapped_column(CHAR(255), comment='失败键')
    test_failtitle: Mapped[str | None] = mapped_column(VARCHAR(255), comment='失败标题')
    test_firmware_v: Mapped[str | None] = mapped_column(CHAR(64), comment='固件版本')
    test_desc: Mapped[str | None] = mapped_column(VARCHAR(255), comment='测试描述')
    test_creatorkey: Mapped[str | None] = mapped_column(VARCHAR(32), comment='创建者键')
    test_modifiedon: Mapped[datetime | None] = mapped_column(DateTime, comment='修改时间')
    test_modifierkey: Mapped[str | None] = mapped_column(CHAR(32), comment='修改者键')
    test_deletedon: Mapped[datetime | None] = mapped_column(DateTime, comment='删除时间')
    test_deleterkey: Mapped[str | None] = mapped_column(CHAR(32), comment='删除者键')
    test_printlock: Mapped[bool] = mapped_column(Boolean().with_variant(INTEGER, 'postgresql'),
                                                 comment='打印锁定状态')
    test_printunlocked_on: Mapped[datetime | None] = mapped_column(DateTime, comment='打印解锁时间')
    test_printunlock_userkey: Mapped[str | None] = mapped_column(CHAR(32), comment='打印解锁用户键')
    test_pass_on1: Mapped[datetime | None] = mapped_column(DateTime, comment='第一次测试通过时间')
    test_pass_testedby1: Mapped[str | None] = mapped_column(CHAR(32), comment='第一次测试执行者')
    test_pass_on2: Mapped[datetime | None] = mapped_column(DateTime, comment='第二次测试通过时间')
    test_pass_testedby2: Mapped[str | None] = mapped_column(CHAR(32), comment='第二次测试执行者')
    test_pass_on3: Mapped[datetime | None] = mapped_column(DateTime, comment='第三次测试通过时间')
    test_pass_testedby3: Mapped[str | None] = mapped_column(CHAR(32), comment='第三次测试执行者')
    test_pass: Mapped[bool] = mapped_column(Boolean().with_variant(INTEGER, 'postgresql'),
                                            comment='总体测试通过状态')
    test_rf_pow: Mapped[Decimal] = mapped_column(  # 新增字段
        DECIMAL(10, 6),
        comment='RF功率'
    )
    test_rf_freqErr: Mapped[Decimal] = mapped_column(  # 新增字段
        DECIMAL(10, 6),
        comment='RF频率误差'
    )
    test_rf_rssi: Mapped[Decimal] = mapped_column(  # 新增字段
        DECIMAL(10, 6),
        comment='RF RSSI'
    )
    test_pow_cur: Mapped[Decimal] = mapped_column(  # 新增字段
        DECIMAL(10, 6),
        comment='电源电流'
    )
    test_pow_volt: Mapped[Decimal] = mapped_column(  # 新增字段
        DECIMAL(10, 6),
        comment='电源电压'
    )
    test_btkey_rssi: Mapped[Decimal] = mapped_column(  # 新增字段
        DECIMAL(10, 6),
        comment='蓝牙键RSSI'
    )
    test_k3orderkey_s: Mapped[str | None] = mapped_column(CHAR(32),
                                                          comment='金蝶source源单单号，生产工单/销售订单')
    test_k3orderkey: Mapped[str | None] = mapped_column(CHAR(32),
                                                        comment='金蝶单据编号，生产入库单/销售出库单')
