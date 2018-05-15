#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-05-15 00:25:26
# @Author  : Wangjojo (wangjojo1995@gmail.com)
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class LoginRequiredMixin(object):
    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)