# -*- coding: UTF-8 -*-
"""
@Project : mespy
@File    : jr_jm03_test.py
@Author  : guhua@jiqid.com
@Date    : 2025/08/26 14:33
"""

from datetime import datetime
from sqlalchemy import Boolean, DateTime, Integer, CHAR, VARCHAR, TEXT, TIMESTAMP, Index
from sqlalchemy.dialects.mysql import TINYINT, INTEGER
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import DataClassBase, id_key


class JRJM03Test(DataClassBase):
    """jm03产品表"""

    __tablename__ = 'jr_jm03_test'

    __table_args__ = (
        # 唯一索引 - 修正名称以匹配DDL
        Index('test_stkey_snkey_times_index', 'test_stkey', 'test_snkey', 'test_times_putin', unique=True),

        # 复合索引
        Index('test_stkey_subkey_index', 'test_stkey', 'test_subkey', 'test_times_putin'),
        Index('test_sn_createdon_index', 'test_createdon', 'test_snkey'),

        # 添加缺失的时间索引
        Index('test_pass_on1_index', 'test_pass_on1'),
        Index('test_pass_on2_index', 'test_pass_on2'),
        Index('test_pass_on3_index', 'test_pass_on3'),

        # 单列索引
        Index('test_wifimac_index', 'test_wifimac'),
        Index('test_subkey_index', 'test_subkey'),
        Index('test_sttitle_index', 'test_sttitle'),
        Index('test_stkey_index', 'test_stkey'),
        Index('test_snkey_index', 'test_snkey'),
        Index('test_skutitle_index', 'test_skutitle'),
        Index('test_skukey_index', 'test_skukey'),
        Index('test_pid_index', 'test_pid'),
        Index('test_key_index', 'test_key'),
        Index('test_did_index', 'test_did'),
        Index('test_createdon_index', 'test_createdon'),
        Index('test_btmac_index', 'test_btmac'),

        # 表注释
        {'comment': 'jm03产品表'}
    )

    test_id: Mapped[id_key] = mapped_column(init=False)

    test_deleted: Mapped[bool] = mapped_column(
        Boolean().with_variant(INTEGER, 'postgresql'),
        comment='是否删除'
    )

    test_createdon: Mapped[datetime | None] = mapped_column(
        TIMESTAMP,
        server_default='CURRENT_TIMESTAMP',
        comment='创建时间'
    )

    test_pid: Mapped[str] = mapped_column(CHAR(32), comment='产品ID')

    # 修正为CHAR(32)以匹配DDL
    test_skukey: Mapped[str] = mapped_column(CHAR(32), comment='序列号唯一键')

    test_pass: Mapped[bool] = mapped_column(
        Boolean().with_variant(INTEGER, 'postgresql'),
        comment='总体测试通过状态'
    )

    test_stkey: Mapped[str] = mapped_column(CHAR(32), comment='序列号键')
    test_sttitle: Mapped[str] = mapped_column(VARCHAR(32), comment='状态标签')
    test_stord: Mapped[int | None] = mapped_column(Integer, comment='状态顺序')
    test_snkey: Mapped[str | None] = mapped_column(CHAR(32), comment='SN键')

    # 修正为CHAR(32)以匹配DDL
    test_subkey: Mapped[str | None] = mapped_column(CHAR(32), comment='绑定的子件物料')

    test_times_putin: Mapped[int | None] = mapped_column(
        Integer,
        comment='BMES成品标识'
    )

    test_pass_1: Mapped[int | None] = mapped_column(
        Integer().with_variant(TINYINT(1), 'mysql'),
        comment='第一轮测试结果: 0-失败, 1-通过, 2-未测试'
    )

    test_pass_2: Mapped[int | None] = mapped_column(
        Integer().with_variant(TINYINT(1), 'mysql'),
        comment='第二轮测试结果: 0-失败, 1-通过, 2-未测试'
    )

    test_pass_3: Mapped[int | None] = mapped_column(
        Integer().with_variant(TINYINT(1), 'mysql'),
        comment='第三轮测试结果: 0-失败, 1-通过, 2-未测试'
    )

    test_info_1: Mapped[str | None] = mapped_column(TEXT, comment='第一轮测试信息')
    test_info_2: Mapped[str | None] = mapped_column(TEXT, comment='第二轮测试信息')
    test_info_3: Mapped[str | None] = mapped_column(TEXT, comment='第三轮测试信息')
    test_pass_on1: Mapped[datetime | None] = mapped_column(DateTime, comment='第一轮测试通过时间')
    test_pass_on2: Mapped[datetime | None] = mapped_column(DateTime, comment='第二轮测试通过时间')
    test_pass_on3: Mapped[datetime | None] = mapped_column(DateTime, comment='第三轮测试通过时间')
    test_pass_testedby1: Mapped[str | None] = mapped_column(CHAR(32), comment='第一轮测试执行者')
    test_pass_testedby2: Mapped[str | None] = mapped_column(CHAR(32), comment='第二轮测试执行者')
    test_pass_testedby3: Mapped[str | None] = mapped_column(CHAR(32), comment='第三轮测试执行者')
    test_wifimac: Mapped[str | None] = mapped_column(CHAR(32), comment='WIFI MAC地址')
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

    test_printlock: Mapped[bool] = mapped_column(
        Boolean().with_variant(INTEGER, 'postgresql'),
        comment='打印锁定状态'
    )

    test_printunlocked_on: Mapped[datetime | None] = mapped_column(DateTime, comment='打印解锁时间')
    test_printunlock_userkey: Mapped[str | None] = mapped_column(CHAR(32), comment='打印解锁用户键')

    test_skutitle: Mapped[str | None] = mapped_column(VARCHAR(128), comment='研究标识')
    test_expired: Mapped[bool] = mapped_column(
        Boolean().with_variant(INTEGER, 'postgresql'),
        comment='是否过期'
    )

    test_btmac: Mapped[str | None] = mapped_column(CHAR(32), comment='bt编码')
    test_did: Mapped[str | None] = mapped_column(CHAR(32), comment='设备ID')
    test_key: Mapped[str | None] = mapped_column(CHAR(32), comment='测试键')

    test_k3orderkey_s: Mapped[str | None] = mapped_column(
        CHAR(32),
        comment='源单单号'
    )

    test_k3orderkey: Mapped[str | None] = mapped_column(
        CHAR(32),
        comment='单据编号'
    )
