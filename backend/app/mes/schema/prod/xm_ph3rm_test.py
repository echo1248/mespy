# -*- coding: UTF-8 -*-
"""
@Project : mespy
@File    : xm_ph3rm_test.py
@Author  : guhua@jiqid.com
@Date    : 2026/06/03 10:20
"""
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class XMPH3RMTestSchemaBase(SchemaBase):
    """ph3rm产品测试基础模型"""

    test_deleted: bool = Field(default=False, description='是否删除')
    test_createdon: datetime | None = Field(default=None, description='创建时间')
    test_pid: str = Field(description='产品ID')
    test_skukey: str = Field(description='SKU键')
    test_skutitle: str | None = Field(default=None, description='SKU标题')
    test_pass: bool = Field(default=False, description='总体测试通过状态')
    test_stkey: str = Field(description='状态键')
    test_sttitle: str | None = Field(default=None, description='状态标题')
    test_stord: int | None = Field(default=None, description='状态顺序')
    test_snkey: str | None = Field(default=None, description='SN键')
    test_subkey: str | None = Field(default=None, description='绑定的子件物料')
    test_times_putin: int | None = Field(default=1, description='投入次数')
    test_pass_1: int | None = Field(default=2, description='第一轮测试结果: 0-失败, 1-通过, 2-未测试')
    test_pass_2: int | None = Field(default=2, description='第二轮测试结果: 0-失败, 1-通过, 2-未测试')
    test_pass_3: int | None = Field(default=2, description='第三轮测试结果: 0-失败, 1-通过, 2-未测试')
    test_info_1: str | None = Field(default=None, description='第一轮测试信息')
    test_info_2: str | None = Field(default=None, description='第二轮测试信息')
    test_info_3: str | None = Field(default=None, description='第三轮测试信息')
    test_pass_on1: datetime | None = Field(default=None, description='第一轮测试通过时间')
    test_pass_on2: datetime | None = Field(default=None, description='第二轮测试通过时间')
    test_pass_on3: datetime | None = Field(default=None, description='第三轮测试通过时间')
    test_pass_testedby1: str | None = Field(default=None, description='第一轮测试执行者')
    test_pass_testedby2: str | None = Field(default=None, description='第二轮测试执行者')
    test_pass_testedby3: str | None = Field(default=None, description='第三轮测试执行者')
    test_wifimac: str | None = Field(default=None, description='WIFI MAC地址')
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
    test_printlock: bool = Field(default=True, description='打印锁定状态')
    test_printunlocked_on: datetime | None = Field(default=None, description='打印解锁时间')
    test_printunlock_userkey: str | None = Field(default=None, description='打印解锁用户键')
    test_k3orderkey_s: str | None = Field(default=None, description='金蝶source源单单号，生产工单/销售订单')
    test_k3orderkey: str | None = Field(default=None, description='金蝶单据编号，生产入库单/销售出库单')
    test_is_rma: bool = Field(default=False, description='是否为RMA返修')
    test_linekey: str | None = Field(default=None, description='产线键')


class CreateXMPH3RMTestParam(XMPH3RMTestSchemaBase):
    """创建ph3rm产品测试参数"""


class UpdateXMPH3RMTestParam(XMPH3RMTestSchemaBase):
    """更新ph3rm产品测试参数"""


class DeleteXMPH3RMTestParam(SchemaBase):
    """删除ph3rm产品测试参数"""

    pks: list[int] = Field(description='ID列表')


class GetXMPH3RMTestDetail(XMPH3RMTestSchemaBase):
    """ph3rm产品测试详情"""

    model_config = ConfigDict(from_attributes=True)

    test_id: int = Field(description='主键ID')
