#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-05-12 03:33:15
# @Author  : Wangjojo (wangjojo1995@gmail.com)
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^detail/(?P<blog_id>\d+)/$',BlogDetailView.as_view(),name = 'blog_detail'),
    url(r'^category/(?P<category_id>\d+)/$',BlogCategoryView.as_view(),name = 'blog_category'),

]