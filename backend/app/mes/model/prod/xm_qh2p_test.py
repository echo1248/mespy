# -*- coding: UTF-8 -*-
"""
@Project : mespy
@File    : xm_qh2p_test.py
@Author  : guhua@jiqid.com
@Date    : 2026/09/03
"""

from datetime import datetime

from sqlalchemy import CHAR, TEXT, TIMESTAMP, VARCHAR, DateTime, Index, Integer, text
from sqlalchemy.dialects.mysql import BIT
from sqlalchemy.dialects.mysql import INTEGER as MYSQL_INTEGER
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import DataClassBase


class XMQH2PTest(DataClassBase):
    """QH2P product test record."""

    __tablename__ = 'xm_qh2p_test'

    __table_args__ = (
        Index('test_stkey_snkey_index', 'test_stkey', 'test_snkey', 'test_times_putin', unique=True),
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
        Index('idx_pid_stkey_createdon', 'test_pid', 'test_stkey', 'test_createdon'),
    )

    test_id: Mapped[int] = mapped_column(
        MYSQL_INTEGER(10, unsigned=True),
        primary_key=True,
        autoincrement=True,
        init=False,
    )
    test_pid: Mapped[str | None] = mapped_column(CHAR(32))
    test_skukey: Mapped[str | None] = mapped_column(CHAR(32))
    test_skutitle: Mapped[str | None] = mapped_column(VARCHAR(128))
    test_expired: Mapped[bool] = mapped_column(
        BIT(1).with_variant(Integer, 'postgresql'),
        server_default=text("b'0'"),
        comment='子件重投后，之前轮次的测试信息过期，置为1',
    )
    test_deleted: Mapped[bool] = mapped_column(
        BIT(1).with_variant(Integer, 'postgresql'),
        server_default=text("b'0'"),
    )
    test_createdon: Mapped[datetime | None] = mapped_column(
        TIMESTAMP,
        server_default=text('CURRENT_TIMESTAMP'),
    )
    test_stkey: Mapped[str] = mapped_column(CHAR(32))
    test_sttitle: Mapped[str | None] = mapped_column(VARCHAR(32))
    test_stord: Mapped[int | None] = mapped_column(MYSQL_INTEGER(11))
    test_snkey: Mapped[str | None] = mapped_column(CHAR(32))
    test_times_putin: Mapped[int] = mapped_column(
        MYSQL_INTEGER(11),
        server_default=text('1'),
        comment='同一个SN，初轮及维修后投入产线轮数',
    )
    test_pass_1: Mapped[int] = mapped_column(
        MYSQL_INTEGER(1),
        server_default=text('2'),
        comment='同一轮投入的第1次测试：0,测试失败，1测试通过，2未测试状态',
    )
    test_pass_2: Mapped[int] = mapped_column(
        MYSQL_INTEGER(1),
        server_default=text('2'),
        comment='同一轮投入的第2次测试：0,测试失败，1测试通过，2未测试状态',
    )
    test_pass_3: Mapped[int] = mapped_column(
        MYSQL_INTEGER(1),
        server_default=text('2'),
        comment='同一轮投入的第3次测试：0,测试失败，1测试通过，2未测试状态',
    )
    test_info_1: Mapped[str | None] = mapped_column(TEXT)
    test_info_2: Mapped[str | None] = mapped_column(TEXT)
    test_info_3: Mapped[str | None] = mapped_column(TEXT)
    test_subkey: Mapped[str | None] = mapped_column(CHAR(64), comment='绑定的子件物料')
    test_wifimac: Mapped[str | None] = mapped_column(CHAR(32))
    test_btmac: Mapped[str | None] = mapped_column(CHAR(32))
    test_did: Mapped[str | None] = mapped_column(CHAR(32))
    test_key: Mapped[str | None] = mapped_column(CHAR(32))
    test_info: Mapped[str | None] = mapped_column(TEXT)
    test_infoecho: Mapped[str | None] = mapped_column(TEXT)
    test_failkey: Mapped[str | None] = mapped_column(CHAR(255))
    test_failtitle: Mapped[str | None] = mapped_column(VARCHAR(255))
    test_firmware_v: Mapped[str | None] = mapped_column(CHAR(64))
    test_desc: Mapped[str | None] = mapped_column(VARCHAR(255))
    test_creatorkey: Mapped[str | None] = mapped_column(VARCHAR(32))
    test_modifiedon: Mapped[datetime | None] = mapped_column(DateTime)
    test_modifierkey: Mapped[str | None] = mapped_column(CHAR(32))
    test_deletedon: Mapped[datetime | None] = mapped_column(DateTime)
    test_deleterkey: Mapped[str | None] = mapped_column(CHAR(32))
    test_printlock: Mapped[bool] = mapped_column(
        BIT(1).with_variant(Integer, 'postgresql'),
        server_default=text("b'1'"),
    )
    test_printunlocked_on: Mapped[datetime | None] = mapped_column(DateTime)
    test_printunlock_userkey: Mapped[str | None] = mapped_column(CHAR(32))
    test_pass_on1: Mapped[datetime | None] = mapped_column(DateTime)
    test_pass_testedby1: Mapped[str | None] = mapped_column(CHAR(32))
    test_pass_on2: Mapped[datetime | None] = mapped_column(DateTime)
    test_pass_testedby2: Mapped[str | None] = mapped_column(CHAR(32))
    test_pass_on3: Mapped[datetime | None] = mapped_column(DateTime)
    test_pass_testedby3: Mapped[str | None] = mapped_column(CHAR(32))
    test_pass: Mapped[bool] = mapped_column(
        BIT(1).with_variant(Integer, 'postgresql'),
        server_default=text("b'0'"),
    )
    test_k3orderkey_s: Mapped[str | None] = mapped_column(
        CHAR(32),
        comment='金蝶source源单单号，生产工单/销售订单',
    )
    test_k3orderkey: Mapped[str | None] = mapped_column(
        CHAR(32),
        comment='金蝶单据编号，生产入库单/销售出库单',
    )
    test_is_rma: Mapped[bool] = mapped_column(
        BIT(1).with_variant(Integer, 'postgresql'),
        server_default=text("b'0'"),
    )
    test_linekey: Mapped[str | None] = mapped_column(CHAR(32))
    test_compuer_ip: Mapped[str | None] = mapped_column(CHAR(64))
    test_compuer_name: Mapped[str | None] = mapped_column(CHAR(64))
