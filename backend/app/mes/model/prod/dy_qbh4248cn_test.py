# -*- coding: UTF-8 -*-
"""
@Project : mespy
@File    : dy_qbh4248cn_test.py
@Author  : guhua@jiqid.com
@Date    : 2025/09/24 13:37
"""

from datetime import datetime
from sqlalchemy import Boolean, DateTime, Integer, CHAR, VARCHAR, TEXT, TIMESTAMP, Index
from sqlalchemy.dialects.mysql import TINYINT, INTEGER
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import DataClassBase, id_key


class DyQBH4248CNTest(DataClassBase):
    """qbh4248cn测试记录表"""

    __tablename__ = 'dy_qbh4248cn_test'

    __table_args__ = (
        # 主键索引（自动创建）

        # 唯一索引
        Index('test_sn_funccode_index', 'test_sn', 'test_funccode', unique=True),

        # 单列索引
        Index('test_key_index', 'test_pcbakey'),
        Index('test_funccode_index', 'test_funccode'),
        Index('test_result_index', 'test_result'),
        Index('test_info_index', 'test_info', mysql_length=50),  # 前缀索引
        Index('test_sn_index', 'test_sn'),
        Index('test_createdon_index', 'test_createdon'),
        Index('test_sn_createdon_index', 'test_sn', 'test_createdon'),

        # 表注释
        {'comment': 'qbh4248cn测试记录表'}
    )

    test_id: Mapped[id_key] = mapped_column(init=False, comment='主键ID')
    test_sn: Mapped[str] = mapped_column(CHAR(32), comment='序列号')
    test_pcbakey: Mapped[str | None] = mapped_column(CHAR(32), comment='PCB板键')
    test_funccode: Mapped[str] = mapped_column(CHAR(32), comment='功能代码')
    test_times_putin: Mapped[int] = mapped_column(Integer, comment='投入次数')
    test_result: Mapped[int] = mapped_column(Integer, comment='测试结果')
    test_result_desc: Mapped[str | None] = mapped_column(TEXT, comment='测试结果描述')
    test_info: Mapped[str | None] = mapped_column(TEXT, comment='测试信息')
    test_info_echo: Mapped[str | None] = mapped_column(
        TEXT, comment='命令执行回响信息'
    )
    test_firmware_v: Mapped[str | None] = mapped_column(CHAR(64), comment='固件版本')
    test_createdon: Mapped[datetime | None] = mapped_column(
        TIMESTAMP, comment='创建时间'
    )
    test_creator: Mapped[str | None] = mapped_column(VARCHAR(32), comment='创建者')
    test_deleted: Mapped[bool] = mapped_column(
        Boolean().with_variant(INTEGER, 'postgresql'), comment='是否删除'
    )
    test_delivered: Mapped[bool] = mapped_column(
        Boolean().with_variant(INTEGER, 'postgresql'), comment='是否已交付'
    )
    test_printlock: Mapped[bool] = mapped_column(
        Boolean().with_variant(INTEGER, 'postgresql'), comment='打印锁定状态'
    )
    test_printunlock_userkey: Mapped[str | None] = mapped_column(
        CHAR(32), comment='打印解锁用户键'
    )
    test_printunlocked_on: Mapped[datetime | None] = mapped_column(
        DateTime, comment='打印解锁时间'
    )
    test_k3orderkey_s: Mapped[str | None] = mapped_column(
        CHAR(32), comment='金蝶source源单单号，生产工单/销售订单'
    )
    test_k3orderkey: Mapped[str | None] = mapped_column(
        CHAR(32), comment='金蝶单据编号，生产入库单/销售出库单'
    )
    test_is_rma: Mapped[bool] = mapped_column(
        Boolean().with_variant(INTEGER, 'postgresql'), comment='是否为RMA返修'
    )
    test_linekey: Mapped[str | None] = mapped_column(CHAR(32), comment='产线键')
