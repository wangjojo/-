#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-05-12 13:17:57
# @Author  : Wangjojo (wangjojo1995@gmail.com)
from .models import Category

home_display_categorys = Category.objects.filter(nav_display = True)

def home_categorys(request):
    return {'home_display_categorys': home_display_categorys}