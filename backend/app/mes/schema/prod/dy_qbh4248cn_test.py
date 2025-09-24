# -*- coding: UTF-8 -*-
"""
@Project : mespy
@File    : dy_qbh4248cn_test.py
@Author  : guhua@jiqid.com
@Date    : 2025/09/24 14:03
"""

from datetime import datetime
from pydantic import ConfigDict, Field
from backend.common.schema import SchemaBase


class DyQBH4248CNTestSchemaBase(SchemaBase):
    """qbh4248cn测试记录基础模型"""

    test_sn: str = Field(description='序列号')
    test_pcbakey: str | None = Field(default=None, description='PCB板键')
    test_funccode: str = Field(description='功能代码')
    test_times_putin: int = Field(default=1, description='投入次数')
    test_result: int = Field(default=0, description='测试结果')
    test_result_desc: str | None = Field(default=None, description='测试结果描述')
    test_info: str | None = Field(default=None, description='测试信息')
    test_info_echo: str | None = Field(default=None, description='命令执行回响信息')
    test_firmware_v: str | None = Field(default=None, description='固件版本')
    test_createdon: datetime | None = Field(default=None, description='创建时间')
    test_creator: str | None = Field(default=None, description='创建者')
    test_deleted: bool = Field(default=False, description='是否删除')
    test_delivered: bool = Field(default=False, description='是否已交付')
    test_printlock: bool = Field(default=True, description='打印锁定状态')
    test_printunlock_userkey: str | None = Field(default=None, description='打印解锁用户键')
    test_printunlocked_on: datetime | None = Field(default=None, description='打印解锁时间')
    test_k3orderkey_s: str | None = Field(default=None, description='金蝶source源单单号，生产工单/销售订单')
    test_k3orderkey: str | None = Field(default=None, description='金蝶单据编号，生产入库单/销售出库单')
    test_is_rma: bool = Field(default=False, description='是否为RMA返修')
    test_linekey: str | None = Field(default=None, description='产线键')


class CreateDyQBH4248CNTestParam(DyQBH4248CNTestSchemaBase):
    """创建qbh4248cn测试记录参数"""


class UpdateDyQBH4248CNTestParam(DyQBH4248CNTestSchemaBase):
    """更新qbh4248cn测试记录参数"""


class DeleteDyQBH4248CNTestParam(SchemaBase):
    """删除qbh4248cn测试记录参数"""

    pks: list[int] = Field(description='ID列表')


class GetDyQBH4248CNTestDetail(DyQBH4248CNTestSchemaBase):
    """qbh4248cn测试记录详情"""

    model_config = ConfigDict(from_attributes=True)

    test_id: int = Field(description='测试ID')
