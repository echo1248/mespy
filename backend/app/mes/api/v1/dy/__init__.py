# -*- coding: UTF-8 -*-
"""
@Project : jiqid-py
@File    : __init__.py.py
@Author  : guhua@jiqid.com
@Date    : 2025/08/19 20:07
"""

from fastapi import APIRouter

from backend.app.mes.api.v1.dy.dy_carton import router as carton
from backend.app.mes.api.v1.dy.dy_pallet import router as pallet

router = APIRouter(prefix='/dy')

router.include_router(carton, prefix='/carton', tags=['纸箱'])
router.include_router(pallet, prefix='/pallet', tags=['栈板'])
