#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Query

from backend.app.mes.schema.prod.dy_qbh4248cn_test import GetDyQBH4248CNTestDetail
from backend.app.mes.service.prod.dy_qbh4248cn_test import dy_qbh4248cn_test_service
from backend.common.pagination import DependsPagination, PageData, paging_data
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.rbac import DependsRBAC
from backend.database.db import CurrentSession

router = APIRouter()


@router.get(
    '',
    summary='分页获取DYQBH',
    dependencies=[
        # DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_dy_qbh4248cn_paged(
        db: CurrentSession,
        test_sn: Annotated[str | None, Query(description='SN键')] = None,
) -> ResponseSchemaModel[PageData[GetDyQBH4248CNTestDetail]]:
    log_select = await dy_qbh4248cn_test_service.get_select(test_sn=test_sn)
    page_data = await paging_data(db, log_select)
    return response_base.success(data=page_data)
