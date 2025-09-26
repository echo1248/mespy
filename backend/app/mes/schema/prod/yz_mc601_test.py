# -*- coding: UTF-8 -*-
"""
@Project : jiqid-py
@File    : yz_mc601_test.py
@Author  : guhua@jiqid.com
@Date    : 2025/08/20 15:27
"""

from datetime import datetime
from decimal import Decimal

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class YZMC601TestSchemaBase(SchemaBase):
    """yz_mc601产品基础模型"""

    test_pid: str | None = Field(default=None, description='产品ID')
    test_skukey: str | None = Field(default=None, description='SKU键')
    test_skutitle: str | None = Field(default=None, description='SKU标题')
    test_expired: bool = Field(default=False, description='子件重投后，之前轮次的测试信息过期，置为1')
    test_deleted: bool = Field(default=False, description='是否删除: 0-未删除, 1-已删除')
    test_createdon: datetime | None = Field(default=None, description='创建时间')
    test_stkey: str = Field(description='测试站键')
    test_sttitle: str | None = Field(default=None, description='测试站标题')
    test_stord: int | None = Field(default=None, description='测试站顺序')
    test_snkey: str | None = Field(default=None, description='序列号键')
    test_times_putin: int = Field(default=1, description='同一个SN，初轮及维修后投入产线轮数')
    test_pass_1: int = Field(default=2, description='同一轮投入的第1次测试：0-测试失败, 1-测试通过, 2-未测试状态')
    test_pass_2: int = Field(default=2, description='同一轮投入的第2次测试：0-测试失败, 1-测试通过, 2-未测试状态')
    test_pass_3: int = Field(default=2, description='同一轮投入的第3次测试：0-测试失败, 1-测试通过, 2-未测试状态')
    test_info_1: str | None = Field(default=None, description='测试信息1')
    test_info_2: str | None = Field(default=None, description='测试信息2')
    test_info_3: str | None = Field(default=None, description='测试信息3')
    test_subkey: str | None = Field(default=None, description='绑定的子件物料')
    test_wifimac: str | None = Field(default=None, description='WIFI MAC地址')
    test_btmac: str | None = Field(default=None, description='蓝牙MAC地址')
    test_did: str | None = Field(default=None, description='设备ID')
    test_key: str | None = Field(default=None, description='测试键')
    test_info: str | None = Field(default=None, description='测试信息')
    test_infoecho: str | None = Field(default=None, description='测试信息回显')
    test_failkey: str | None = Field(default=None, description='失败键')
    test_failtitle: str | None = Field(default=None, description='失败标题')
    test_firmware_v: str | None = Field(default=None, description='固件版本')
    test_desc: str | None = Field(default=None, description='测试描述')
    test_creatorkey: str | None = Field(default=None, description='创建者键')
    test_modifiedon: datetime | None = Field(default=None, description='修改时间')
    test_modifierkey: str | None = Field(default=None, description='修改者键')
    test_deletedon: datetime | None = Field(default=None, description='删除时间')
    test_deleterkey: str | None = Field(default=None, description='删除者键')
    test_printlock: bool = Field(default=False, description='打印锁定状态')
    test_printunlocked_on: datetime | None = Field(default=None, description='打印解锁时间')
    test_printunlock_userkey: str | None = Field(default=None, description='打印解锁用户键')
    test_pass_on1: datetime | None = Field(default=None, description='第一次测试通过时间')
    test_pass_testedby1: str | None = Field(default=None, description='第一次测试执行者')
    test_pass_on2: datetime | None = Field(default=None, description='第二次测试通过时间')
    test_pass_testedby2: str | None = Field(default=None, description='第二次测试执行者')
    test_pass_on3: datetime | None = Field(default=None, description='第三次测试通过时间')
    test_pass_testedby3: str | None = Field(default=None, description='第三次测试执行者')
    test_pass: bool = Field(default=False, description='总体测试通过状态')

    # 修复：为不能为null的字段添加合适的默认值
    test_rf_pow: Decimal = Field(default=Decimal('0.0'), description='RF功率')
    test_rf_freqErr: Decimal = Field(default=Decimal('0.0'), description='RF频率误差')
    test_rf_rssi: Decimal = Field(default=Decimal('0.0'), description='RF RSSI')
    test_pow_cur: Decimal = Field(default=Decimal('0.0'), description='电源电流')
    test_pow_volt: Decimal = Field(default=Decimal('0.0'), description='电源电压')
    test_btkey_rssi: Decimal = Field(default=Decimal('0.0'), description='蓝牙键RSSI')

    test_k3orderkey_s: str | None = Field(default=None, description='金蝶source源单单号，生产工单/销售订单')
    test_k3orderkey: str | None = Field(default=None, description='金蝶单据编号，生产入库单/销售出库单')


class CreateYZMC601TestParam(YZMC601TestSchemaBase):
    """创建yz_mc601产品测试参数"""


class UpdateYZMC601TestParam(YZMC601TestSchemaBase):
    """更新yz_mc601产品测试参数"""


class DeleteYZMC601TestParam(SchemaBase):
    """删除yz_mc601产品测试参数"""

    pks: list[int] = Field(description='ID列表')


class GetYZMC601TestDetail(YZMC601TestSchemaBase):
    """yz_mc601产品测试详情"""

    model_config = ConfigDict(from_attributes=True)

    test_id: int = Field(description='测试ID')
