# -*- coding: UTF-8 -*-

import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from backend.core.conf import settings
import asyncio


class EmailService(object):

    def __init__(self):
        self.from_address = settings.EMAIL["from_address"]
        self.password = settings.EMAIL["password"]
        self.subject = settings.EMAIL["subject"]

    async def send_msg(self, receivers, body):
        html_body = f"""
        <html><body>
            <p>你好：</p>
            <div style="margin-left: 20px; padding: 10px;">{body}</div>
        </body></html>
        """
        content = {"data": html_body, "type": "html"}
        await self.send(receivers, content, self.subject, self.from_address)

    async def send(self, receivers, content, subject, from_address, email_files=None):
        """发送邮件"""
        msg = MIMEMultipart()
        msg['From'] = from_address
        msg['To'] = ",".join(receivers)
        msg['Subject'] = subject

        msg.attach(MIMEText(content["data"], content["type"], 'utf-8'))

        await aiosmtplib.send(
            msg, hostname="smtp.exmail.qq.com", port=25, username=self.from_address, password=self.password,
        )


email_service = EmailService()


# async def main():
#     await email_service.send_msg(
#         receivers=["guhua@jiqid.com"],
#         body="MES Monitor ISC精细化管理接口上报预警"
#     )
#
#
# if __name__ == '__main__':
#     asyncio.run(main())
