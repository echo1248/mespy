# -*- coding: UTF-8 -*-
"""
@Project : mespy
@File    : xm_m11a_test.py
@Author  : guhua@jiqid.com
@Date    : 2025/08/26 14:24
"""
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class XMM11ATestSchemaBase(SchemaBase):
    """M11A产品基础模型"""

    test_deleted: bool = Field(default=False, description='是否删除')
    test_createdon: datetime | None = Field(default=None, description='创建时间')
    test_pid: str = Field(description='产品ID')
    test_skukey: str = Field(description='序列号唯一键')
    test_pass: bool = Field(default=False, description='总体测试通过状态')
    test_stkey: str = Field(description='序列号键')
    test_sttitle: str | None = Field(default=None, description='状态标签')
    test_stord: int | None = Field(default=None, description='状态顺序')
    test_snkey: str | None = Field(default=None, description='SN键')
    test_subkey: str | None = Field(default=None, description='绑定的子件物料')
    test_times_putin: int | None = Field(default=None, description='BMES成品标识')
    test_pass_1: int | None = Field(default=None, description='第一轮测试结果: 0-失败, 1-通过, 2-未测试')
    test_pass_2: int | None = Field(default=None, description='第二轮测试结果: 0-失败, 1-通过, 2-未测试')
    test_pass_3: int | None = Field(default=None, description='第三轮测试结果: 0-失败, 1-通过, 2-未测试')
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
    test_printlock: bool = Field(default=False, description='打印锁定状态')
    test_printunlocked_on: datetime | None = Field(default=None, description='打印解锁时间')
    test_printunlock_userkey: str | None = Field(default=None, description='打印解锁用户键')


class CreateXMM11ATestParam(XMM11ATestSchemaBase):
    """创建M11A产品测试参数"""


class UpdateXMM11ATestParam(XMM11ATestSchemaBase):
    """更新M11A产品测试参数"""


class DeleteXMM11ATestParam(SchemaBase):
    """删除M11A产品测试参数"""

    pks: list[int] = Field(description='ID列表')


class GetXMM11ATestDetail(XMM11ATestSchemaBase):
    """M11A产品测试详情"""

    model_config = ConfigDict(from_attributes=True)

    test_id: int = Field(description='主键ID')
