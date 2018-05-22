#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-05-22 21:54:58
# @Author  : Wangjojo (wangjojo1995@gmail.com)
def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])

    return [b"Hello World"] # python3