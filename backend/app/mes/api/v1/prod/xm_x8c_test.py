#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Query

from backend.app.mes.schema.prod.xm_x8c_test import GetXMX8CTestDetail
from backend.app.mes.service.prod.xm_x8c_test import xm_x8c_test_service
from backend.common.pagination import DependsPagination, PageData, paging_data
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.rbac import DependsRBAC
from backend.database.db import CurrentSession

router = APIRouter()


@router.get(
    '',
    summary='分页获取XMX8C',
    dependencies=[
        # DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_xm_x8c_paged(
        db: CurrentSession,
        test_snkey: Annotated[str | None, Query(description='SN键')] = None,
) -> ResponseSchemaModel[PageData[GetXMX8CTestDetail]]:
    log_select = await xm_x8c_test_service.get_select(test_snkey=test_snkey)
    page_data = await paging_data(db, log_select)
    return response_base.success(data=page_data)
