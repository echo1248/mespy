import asyncio
import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from sqlalchemy import text
from backend.core.conf import settings
from backend.common.log import log

from backend.app.task.celery import celery_app
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
    log.info("📨 [task_email_send] 开始执行存储过程并准备发送邮件")
    try:
        async with async_db_session.begin() as session:
            await session.execute(text("SET @ret = '';"))
            await session.execute(text("CALL procISC_DeleteHistoryAndCheckHB(@ret);"))
            result = await session.execute(text("SELECT @ret AS ret;"))
            row = result.fetchone()
            await session.commit()

        ret_msg = row.ret if row and row.ret else "无返回结果"
        if row and row.ret:
            await send_email(
                recipients=["wangzhong@jiqid.com", ],
                body=f"MES Monitor ISC精细化管理接口上报预警 - {ret_msg}",
                subject="MES 系统邮件",
                cc_recipients=["guhua@jiqid.com", ],
            )

        log.info(f"✅ [task_email_send] 执行成功，结果：{ret_msg}")
        return ret_msg
    except Exception as e:
        log.error(f"❌ [task_email_send] 任务执行失败: {e}", exc_info=True)
        return "任务执行失败"


async def send_email(
        recipients: list[str],
        body: str,
        subject: str,
        cc_recipients: list[str] | None = None
):
    """发送邮件"""
    if not recipients:
        log.error("发送邮件失败: 收件人列表为空")
        return

    html_body = f"""
<html>
<body>
    <p>你好：</p>
    <div>{body}</div>
    <br>
    <p><i>系统自动邮件，请勿回复</i></p>
</body>
</html>
"""
    try:
        msg = MIMEMultipart('mixed')
        msg['From'] = settings.EMAIL_USERNAME
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = subject

        if cc_recipients:
            msg['Cc'] = ", ".join(cc_recipients)

        msg.attach(MIMEText(html_body, "html", 'utf-8'))

        await aiosmtplib.send(
            msg, hostname=settings.EMAIL_HOST, port=settings.EMAIL_PORT,
            username=settings.EMAIL_USERNAME, password=settings.EMAIL_PASSWORD,
        )
    except Exception as e:
        log.error(f"邮件发送失败: {str(e)}, 收件人={recipients}, 主题={subject}")
