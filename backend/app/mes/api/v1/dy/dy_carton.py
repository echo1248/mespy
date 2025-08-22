#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Query

from backend.app.mes.schema.dy_carton import DeleteDyCartonParam, GetDyCartonDetail
from backend.app.mes.service.dy_carton import dy_carton_service
from backend.common.pagination import DependsPagination, PageData, paging_data
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.rbac import DependsRBAC
from backend.database.db import CurrentSession

router = APIRouter()


@router.get(
    '',
    summary='分页获取箱号',
    dependencies=[
        # DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_cartons_paged(
        db: CurrentSession,
        carton_key: Annotated[str | None, Query(description='箱号(箱标)')] = None,
) -> ResponseSchemaModel[PageData[GetDyCartonDetail]]:
    log_select = await dy_carton_service.get_select(carton_key=carton_key)
    page_data = await paging_data(db, log_select)
    return response_base.success(data=page_data)
