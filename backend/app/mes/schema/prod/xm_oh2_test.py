# -*- coding: UTF-8 -*-
"""
@Project : jiqid-py
@File    : xm_oh2_test.py
@Author  : guhua@jiqid.com
@Date    : 2025/08/20 15:27
"""

from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class XMOH2TestSchemaBase(SchemaBase):
    """oh2产品基础模型"""

    test_pid: str = Field(description='产品ID')
    test_skukey: str = Field(description='序列号唯一键')
    test_skutitle: str | None = Field(description='研究标识')
    test_expired: bool = Field(default=False, description='是否过期')
    test_deleted: bool = Field(default=False, description='是否删除')
    test_createdon: datetime | None = Field(default=None, description='创建时间')
    test_stkey: str = Field(description='序列号键')
    test_sttitle: str = Field(description='状态标签')
    test_stord: int | None = Field(default=None, description='状态顺序')
    test_snkey: str = Field(description='SN键')
    test_times_putin: int = Field(default=1, description='投入次数')
    test_pass_1: int = Field(default=1, description='第一轮测试结果: 0-失败, 1-通过, 2-未测试')
    test_pass_2: int = Field(default=2, description='第二轮测试结果: 0-失败, 1-通过, 2-未测试')
    test_pass_3: int = Field(default=2, description='第三轮测试结果: 0-失败, 1-通过, 2-未测试')
    test_info_1: str | None = Field(default=None, description='第一轮测试信息')
    test_info_2: str | None = Field(default=None, description='第二轮测试信息')
    test_info_3: str | None = Field(default=None, description='第三轮测试信息')
    test_subkey: str | None = Field(default=None, description='子件键')
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
    test_pass_on1: datetime | None = Field(default=None, description='第一轮测试通过时间')
    test_pass_testedby1: str | None = Field(default=None, description='第一轮测试执行者')
    test_pass_on2: datetime | None = Field(default=None, description='第二轮测试通过时间')
    test_pass_testedby2: str | None = Field(default=None, description='第二轮测试执行者')
    test_pass_on3: datetime | None = Field(default=None, description='第三轮测试通过时间')
    test_pass_testedby3: str | None = Field(default=None, description='第三轮测试执行者')
    test_pass: bool = Field(default=False, description='总体测试通过状态')
    test_orderkey_s: str | None = Field(default=None, description='订单号(溯源)')
    test_orderkey: str | None = Field(default=None, description='订单号')


class CreateXMOH2TestParam(XMOH2TestSchemaBase):
    """创建oh2产品测试参数"""


class UpdateXMOH2TestParam(XMOH2TestSchemaBase):
    """更新oh2产品测试参数"""


class DeleteXMOH2TestParam(SchemaBase):
    """删除oh2产品测试参数"""

    pks: list[int] = Field(description='ID列表')


class GetXMOH2TestDetail(XMOH2TestSchemaBase):
    """oh2产品测试详情"""

    model_config = ConfigDict(from_attributes=True)

    test_id: int = Field(description='测试ID')
