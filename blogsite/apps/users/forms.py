#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-05-12 17:21:02
# @Author  : Wangjojo (wangjojo1995@gmail.com)
from django import forms

from .models import UserProfile
from captcha.fields import CaptchaField

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=6)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=6)
    captcha = CaptchaField(error_messages={'invalid':'验证码错误'})


class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages ={'invalid':'验证码错误'})

class ResetPwdForm(forms.Form):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(required=True,min_length=6)
    password2 = forms.CharField(required=True,min_length=6)