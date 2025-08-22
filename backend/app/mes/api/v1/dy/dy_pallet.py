#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated, List

from fastapi import APIRouter, Query

from backend.app.mes.schema.dy_pallet import DeleteDyPalletParam, GetDyPalletDetail, BillParamList
from backend.app.mes.service.dy_pallet import dy_pallet_service
from backend.common.pagination import DependsPagination, PageData, paging_data
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.rbac import DependsRBAC
from backend.database.db import CurrentSession

router = APIRouter()


@router.post(
    '/approve_in_bill',
    summary='入库审核',
    dependencies=[
    ],
)
async def approve_in_bill(
        db: CurrentSession,
        bill_params: BillParamList,
) -> ResponseModel:
    await dy_pallet_service.approve_in_bill(bill_params=bill_params.items)
    return response_base.success()


@router.post(
    '/reverse_in_bill',
    summary='入库反审核',
    dependencies=[
    ],
)
async def reverse_in_bill(
        db: CurrentSession,
        bill_params: BillParamList,
) -> ResponseModel:
    await dy_pallet_service.reverse_in_bill(bill_params=bill_params.items)
    return response_base.success()


@router.post(
    '/approve_out_bill',
    summary='出库审核',
    dependencies=[
    ],
)
async def approve_out_bill(
        db: CurrentSession,
        bill_params: BillParamList,
) -> ResponseModel:
    await dy_pallet_service.approve_out_bill(bill_params=bill_params.items)
    return response_base.success()


@router.post(
    '/reverse_out_bill',
    summary='出库反审核',
    dependencies=[
    ],
)
async def reverse_out_bill(
        db: CurrentSession,
        bill_params: BillParamList,
) -> ResponseModel:
    await dy_pallet_service.reverse_out_bill(bill_params=bill_params.items)
    return response_base.success()


@router.get(
    '',
    summary='分页获取栈板',
    dependencies=[
        # DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_pallets_paged(
        db: CurrentSession,
        pallet_pid: Annotated[str | None, Query(description='产品id')] = None,
        pallet_key: Annotated[str | None, Query(description='栈板标')] = None,
) -> ResponseSchemaModel[PageData[GetDyPalletDetail]]:
    log_select = await dy_pallet_service.get_select(pallet_pid=pallet_pid, pallet_key=pallet_key)
    page_data = await paging_data(db, log_select)
    return response_base.success(data=page_data)
