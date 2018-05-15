#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-05-14 18:45:24
# @Author  : Wangjojo (wangjojo1995@gmail.com)
from random import randint


from django.core.mail import send_mail
from blogsite.settings import DEFAULT_FROM_EMAIL

from users.models import EmailVerifyRecord

def random_code(randomlength):
    code = ''
    chars = 'qwertyuiopasdfghjklzxcvbnm1234567890'
    length = len(chars)-1
    for i in range(randomlength):
        code += chars[randint(0,length)]
    return code

def send_user_email(email,send_type = 'register'):
    email_record = EmailVerifyRecord()
    #生成邮件并保存记录
    if send_type == 'update_email':

        code = random_code(4)
    else:
        code = random_code(16)

    email_record.email = email
    email_record.code = code
    email_record.send_type = send_type
    email_record.save()

    #发送邮件
    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = 'wangjojo注册激活链接'
        email_body = '访问链接，登录账号：http://192.168.74.136:8001/active/{0}'.format(code)

        send_status = send_mail(email_title,email_body,DEFAULT_FROM_EMAIL,[email])

        if send_status:
            pass

    elif send_type == 'forget':
        email_title = 'wangjojo重置密码链接'
        email_body = '访问链接，重置密码：http://192.168.74.136:8001/reset/{0}'.format(code)

        send_status = send_mail(email_title,email_body,DEFAULT_FROM_EMAIL,[email])

        if send_status:
            pass

    elif send_type == 'update_email':
        email_title = 'wangjojo更新邮箱验证码'
        email_body = '你的验证码为：{0}'.format(code)

        send_status = send_mail(email_title,email_body,DEFAULT_FROM_EMAIL,[email])

        if send_status:
            pass