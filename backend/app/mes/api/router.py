# -*- coding: UTF-8 -*-
"""
@Project : jiqid-py
@File    : router.py
@Author  : guhua@jiqid.com
@Date    : 2025/08/12 09:44
"""

from fastapi import APIRouter
from backend.core.conf import settings

from backend.app.mes.api.v1.dy import router as dy_router
from backend.app.mes.api.v1.prod import router as prod_router

v1 = APIRouter(prefix=f'{settings.FASTAPI_API_V1_PATH}/mes')

v1.include_router(dy_router)
v1.include_router(prod_router)
