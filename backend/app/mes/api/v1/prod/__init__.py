# -*- coding: UTF-8 -*-
"""
@Project : jiqid-py
@File    : __init__.py.py
@Author  : guhua@jiqid.com
@Date    : 2025/08/20 15:51
"""

from fastapi import APIRouter

from backend.app.mes.api.v1.prod.jr_jm03_test import router as jr_jm03
from backend.app.mes.api.v1.prod.xm_l05b_test import router as xm_l05b
from backend.app.mes.api.v1.prod.xm_m11a_test import router as xm_m11a
from backend.app.mes.api.v1.prod.xm_oh2_test import router as xm_oh2
from backend.app.mes.api.v1.prod.xm_oh3r_test import router as xm_oh3r
from backend.app.mes.api.v1.prod.xm_oh11_test import router as xm_oh11
from backend.app.mes.api.v1.prod.xm_x4b_test import router as xm_x4b
from backend.app.mes.api.v1.prod.xm_x6a_test import router as xm_x6a
from backend.app.mes.api.v1.prod.xm_x8c_test import router as xm_x8c
from backend.app.mes.api.v1.prod.xm_x8f_test import router as xm_x8f
from backend.app.mes.api.v1.prod.yz_mc60_01_test import router as yz_mc60_01
from backend.app.mes.api.v1.prod.yz_mc601_test import router as yz_mc601
from backend.app.mes.api.v1.prod.xm_xhb_test import router as xm_xhb
from backend.app.mes.api.v1.prod.dy_qbh4248cn_test import router as dy_qbh4248cn

router = APIRouter(prefix='/prod')

router.include_router(jr_jm03, prefix='/jr_jm03', tags=['jr_jm03'])
router.include_router(xm_l05b, prefix='/xm_l05b', tags=['xm_l05b'])
router.include_router(xm_m11a, prefix='/xm_m11a', tags=['xm_m11a'])
router.include_router(xm_oh2, prefix='/xm_oh2', tags=['xm_oh2'])
router.include_router(xm_oh3r, prefix='/xm_oh3r', tags=['xm_oh3r'])
router.include_router(xm_oh11, prefix='/xm_oh11', tags=['xm_oh11'])
router.include_router(xm_x4b, prefix='/xm_x4b', tags=['xm_x4b'])
router.include_router(xm_x6a, prefix='/xm_x6a', tags=['xm_x6a'])
router.include_router(xm_x8c, prefix='/xm_x8c', tags=['xm_x8c'])
router.include_router(xm_x8f, prefix='/xm_x8f', tags=['xm_x8f'])
router.include_router(yz_mc60_01, prefix='/yz_mc60_01', tags=['yz_mc60_01'])
router.include_router(yz_mc601, prefix='/yz_mc601', tags=['yz_mc601'])
router.include_router(xm_xhb, prefix='/xm_xhb', tags=['xm_xhb'])
router.include_router(dy_qbh4248cn, prefix='/dy_qbh4248cn', tags=['dy_qbh4248cn'])
