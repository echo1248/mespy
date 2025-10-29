# -*- coding: UTF-8 -*-
from typing import List, Any, Dict

import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from backend.common.log import log
from backend.core.conf import settings
import asyncio


class EmailService(object):

    def __init__(self):
        self.hostname = settings.EMAIL_HOST
        self.port = settings.EMAIL_PORT
        self.username = settings.EMAIL_USERNAME
        self.password = settings.EMAIL_PASSWORD

    async def send(self, recipients, body):
        html_body = f"""
        <html><body>
            <p>你好：</p>
            <div style="margin-left: 20px; padding: 10px;">{body}</div>
        </body></html>
        """
        content = {"data": html_body, "type": "html"}
        await self._send(recipients, content)

    async def _send(
            self,
            recipients: List[str],
            content: Dict[str, Any],
            subject: str = "MES 系统邮件"
    ):
        """发送邮件"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = ",".join(recipients)
            msg['Subject'] = subject

            msg.attach(MIMEText(content["data"], content["type"], 'utf-8'))

            await aiosmtplib.send(
                msg, hostname=self.hostname, port=self.port,
                username=self.username, password=self.password,
            )
        except Exception as e:
            log.error(f"邮件发送失败: {str(e)}, 收件人={recipients}, 主题={subject}")
            return False


email_service = EmailService()


async def main():
    await email_service.send(
        recipients=["guhua@jiqid.com"],
        body="MES Monitor ISC精细化管理接口上报预警"
    )


if __name__ == '__main__':
    asyncio.run(main())
