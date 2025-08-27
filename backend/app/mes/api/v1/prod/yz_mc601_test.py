#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Query

from backend.app.mes.schema.prod.yz_mc601_test import GetYZMC601TestDetail
from backend.app.mes.service.prod.yz_mc601_test import yz_mc601_test_service
from backend.common.pagination import DependsPagination, PageData, paging_data
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.rbac import DependsRBAC
from backend.database.db import CurrentSession

router = APIRouter()


@router.get(
    '',
    summary='分页获取YZMC601',
    dependencies=[
        # DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_yz_mc601_paged(
        db: CurrentSession,
        test_snkey: Annotated[str | None, Query(description='SN键')] = None,
) -> ResponseSchemaModel[PageData[GetYZMC601TestDetail]]:
    log_select = await yz_mc601_test_service.get_select(test_snkey=test_snkey)
    page_data = await paging_data(db, log_select)
    return response_base.success(data=page_data)
