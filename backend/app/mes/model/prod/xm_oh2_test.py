# -*- coding: UTF-8 -*-
"""
@Project : jiqid-py
@File    : xm_oh2_test.py
@Author  : your_name@your_company.com
@Date    : 2025/08/20 14:30
"""

from datetime import datetime
from sqlalchemy import Boolean, DateTime, Integer, CHAR, VARCHAR, TEXT, TIMESTAMP, Index
from sqlalchemy.dialects.mysql import TINYINT, INTEGER
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import DataClassBase, id_key


class XMOH2Test(DataClassBase):
    """oh2产品表"""

    __tablename__ = 'xm_oh2_test'

    __table_args__ = (
        # 唯一索引
        Index('test_stkey_snkey_index', 'test_stkey', 'test_snkey', 'test_times_putin', unique=True),

        # 复合索引
        Index('test_stkey_subkey_index', 'test_stkey', 'test_subkey', 'test_times_putin'),
        Index('test_sn_createdon_index', 'test_createdon', 'test_snkey'),

        # 单列索引
        Index('test_wifimac_index', 'test_wifimac'),
        Index('test_subkey_idnex', 'test_subkey'),
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
        {'comment': 'oh2产品表'}
    )

    test_id: Mapped[id_key] = mapped_column(init=False, comment='主键ID')
    test_pid: Mapped[str] = mapped_column(CHAR(32), comment='产品ID')
    test_skukey: Mapped[str] = mapped_column(CHAR(32), comment='序列号唯一键')
    test_skutitle: Mapped[str] = mapped_column(VARCHAR(128), comment='研究标识')
    test_expired: Mapped[bool] = mapped_column(
        Boolean().with_variant(INTEGER, 'postgresql'), comment='是否过期'
    )
    test_deleted: Mapped[bool] = mapped_column(
        Boolean().with_variant(INTEGER, 'postgresql'), comment='是否删除'
    )
    test_createdon: Mapped[datetime | None] = mapped_column(TIMESTAMP, comment='创建时间')
    test_stkey: Mapped[str] = mapped_column(CHAR(32), comment='序列号键')
    test_sttitle: Mapped[str] = mapped_column(VARCHAR(32), comment='状态标签')
    test_stord: Mapped[int] = mapped_column(Integer, comment='状态顺序')
    test_snkey: Mapped[str] = mapped_column(CHAR(32), comment='SN键')
    test_times_putin: Mapped[int] = mapped_column(Integer, comment='BMES成品标识')
    test_pass_1: Mapped[int] = mapped_column(
        Integer().with_variant(TINYINT(1), 'mysql'), comment='第一轮测试结果: 0-失败, 1-通过, 2-未测试'
    )
    test_pass_2: Mapped[int] = mapped_column(
        Integer().with_variant(TINYINT(1), 'mysql'), comment='第二轮测试结果: 0-失败, 1-通过, 2-未测试'
    )
    test_pass_3: Mapped[int] = mapped_column(
        Integer().with_variant(TINYINT(1), 'mysql'), comment='第三轮测试结果: 0-失败, 1-通过, 2-未测试'
    )
    test_info_1: Mapped[str] = mapped_column(TEXT, comment='第一轮测试信息')
    test_info_2: Mapped[str] = mapped_column(TEXT, comment='第二轮测试信息')
    test_info_3: Mapped[str] = mapped_column(TEXT, comment='第三轮测试信息')
    test_subkey: Mapped[str] = mapped_column(CHAR(64), comment='序列号唯一键2')
    test_wifimac: Mapped[str] = mapped_column(CHAR(32), comment='WIFI MAC地址')
    test_btmac: Mapped[str] = mapped_column(CHAR(32), comment='bt编码')
    test_did: Mapped[str] = mapped_column(CHAR(32), comment='设备ID')
    test_key: Mapped[str] = mapped_column(CHAR(32), comment='测试键')
    test_info: Mapped[str] = mapped_column(TEXT, comment='测试信息')
    test_infoecho: Mapped[str] = mapped_column(TEXT, comment='测试信息回显')
    test_failkey: Mapped[str] = mapped_column(CHAR(255), comment='失败键')
    test_failtitle: Mapped[str] = mapped_column(VARCHAR(255), comment='失败标题')
    test_firmware_v: Mapped[str] = mapped_column(CHAR(64), comment='固件版本')
    test_desc: Mapped[str] = mapped_column(VARCHAR(255), comment='测试描述')
    test_creatorkey: Mapped[str | None] = mapped_column(VARCHAR(32), comment='创建者键')
    test_modifiedon: Mapped[datetime | None] = mapped_column(DateTime, comment='修改时间')
    test_modifierkey: Mapped[str] = mapped_column(CHAR(32), comment='修改者键')
    test_deletedon: Mapped[datetime | None] = mapped_column(DateTime, comment='删除时间')
    test_deleterkey: Mapped[str] = mapped_column(CHAR(32), comment='删除者键')
    test_printlock: Mapped[bool] = mapped_column(
        Boolean().with_variant(INTEGER, 'postgresql'), comment='打印锁定状态'
    )
    test_printunlocked_on: Mapped[datetime | None] = mapped_column(DateTime, comment='打印解锁时间')
    test_printunlock_userkey: Mapped[str] = mapped_column(CHAR(32), comment='打印解锁用户键')
    test_pass_on1: Mapped[datetime | None] = mapped_column(DateTime, comment='第一轮测试通过时间')
    test_pass_testedby1: Mapped[str] = mapped_column(CHAR(32), comment='第一轮测试执行者')
    test_pass_on2: Mapped[datetime | None] = mapped_column(DateTime, comment='第二轮测试通过时间')
    test_pass_testedby2: Mapped[str] = mapped_column(CHAR(32), comment='第二轮测试执行者')
    test_pass_on3: Mapped[datetime | None] = mapped_column(DateTime, comment='第三轮测试通过时间')
    test_pass_testedby3: Mapped[str] = mapped_column(CHAR(32), comment='第三轮测试执行者')
    test_pass: Mapped[bool] = mapped_column(
        Boolean().with_variant(INTEGER, 'postgresql'), comment='总体测试通过状态'
    )
    test_k3orderkey_s: Mapped[str | None] = mapped_column(CHAR(32),
                                                          comment='金蝶source源单单号，生产工单/销售订单')
    test_k3orderkey: Mapped[str | None] = mapped_column(CHAR(32),
                                                        comment='金蝶单据编号，生产入库单/销售出库单')
