#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-05-12 03:33:15
# @Author  : Wangjojo (wangjojo1995@gmail.com)
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^detail/(?P<blog_id>\d+)/$',BlogDetailView.as_view(),name = 'blog_detail'),
    url(r'^category/(?P<category_id>\d+)/$',BlogCategoryView.as_view(),name = 'blog_category'),
    url(r'^author/(?P<author_id>\d+)/$',BlogAuthorView.as_view(),name = 'blog_author'),
    #归档
    url(r'^archvies/(?P<year>\d+)/(?P<month>\d+)/$',ArchivesView.as_view(),name = 'blog_archives'),
    #标签云
    url(r'^tag/(?P<tag_id>\d+)/$',BlogTagView.as_view(),name = 'blog_tag'), 
    #添加评论
    url(r'^add_comment/$',AddCommentView.as_view(),name = 'add_comment'),
    #全局搜索
    url(r'^search/list/$',SearchView.as_view(),name = 'search_list'),    

]