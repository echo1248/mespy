import asyncio

from sqlalchemy import text
from backend.common.log import log

from backend.app.task.celery import celery_app
from backend.app.task.utils.email_util import email_service
from backend.database.db import async_db_session


@celery_app.task(name='task_demo')
def task_demo() -> str:
    """示例任务，模拟耗时操作"""
    log.info("开始同步示例任务")
    return 'test async'


@celery_app.task(name='task_demo_async')
async def task_demo_async() -> str:
    """异步示例任务，模拟耗时操作"""
    log.info("开始异步示例任务")
    return 'test async'


@celery_app.task(name='task_demo_params')
async def task_demo_params(hello: str, world: str | None = None) -> str:
    """参数示例任务，模拟传参操作"""
    log.info("开始参数示例任务")
    return hello + world


@celery_app.task(name="task_email_send")
async def task_email_send() -> str:
    """执行存储过程并发送邮件通知"""
    return await asyncio.wait_for(_task_email_send_async(), timeout=60)


async def _task_email_send_async():
    log.info("📨 [task_email_send] 开始执行存储过程并准备发送邮件")

    try:
        async with async_db_session.begin() as session:
            await session.execute(text("SET @ret = '';"))
            await session.execute(text("CALL procISC_DeleteHistoryAndCheckHB(@ret);"))
            result = await session.execute(text("SELECT @ret AS ret;"))
            row = result.fetchone()
            await session.commit()

        ret_msg = row.ret if row and row.ret else "无返回结果"

        # 发送邮件
        if row and row.ret:
            await email_service.send(
                recipients=["wangzhong@jiqid.com", "guhua@jiqid.com"],
                body=f"MES Monitor ISC精细化管理接口上报预警 - {ret_msg}"
            )

        log.info(f"✅ [task_email_send] 执行成功，结果：{ret_msg}")

        return ret_msg

    except Exception as e:
        log.error(f"❌ [task_email_send] 任务执行失败: {e}", exc_info=True)
