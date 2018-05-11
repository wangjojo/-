#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-05-11 15:21:52
# @Author  : Wangjojo (wangjojo1995@gmail.com)
from .models import *

import xadmin

class BlogCommentsAdmin(object):
    '''
        Admin View for BlogComments
    '''
    list_display = ('user','blog','content','add_time')
    list_filter = ('user','blog','content','add_time')
    search_fields = ('user__username','blog','content')


class UserFavAdmin(object):
    '''
        Admin View for UserFav
    '''
    list_display = ('user','fav_id','fav_type','add_time')
    list_filter = ('user','fav_id','fav_type','add_time')
    search_fields = ('user_username','fav_id','fav_type')


class UserMessageAdmin(object):
    '''
        Admin View for UserMessage
    '''
    list_display = ('user','message','has_read','add_time')
    list_filter = ('user','message','has_read','add_time')
    search_fields = ('user__username','message','has_read')


class UserBlogAdmin(object):
    '''
        Admin View for UserBlog
    '''
    list_display = ('user','blog','add_time')
    list_filter = ('user','blog','add_time')
    search_fields = ('user__username','blog__title',)


xadmin.site.register(BlogComments, BlogCommentsAdmin)
xadmin.site.register(UserFav, UserFavAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserBlog, UserBlogAdmin)

