# -*- coding: UTF-8 -*-
"""
@Project : jiqid-py
@File    : __init__.py.py
@Author  : guhua@jiqid.com
@Date    : 2025/08/20 15:51
"""

from fastapi import APIRouter

from backend.app.mes.api.v1.prod.xm_oh2_test import router as xm_oh2

router = APIRouter(prefix='/prod')

router.include_router(xm_oh2, prefix='/xm_oh2', tags=['XM_OH2'])
