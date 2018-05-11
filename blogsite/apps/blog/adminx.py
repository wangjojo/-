#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-05-11 13:28:18
# @Author  : Wangjojo (wangjojo1995@gmail.com)
from .models import *

import xadmin

class CategoryAdmin(object):
    '''
        Admin View for Category
    '''
    list_display = ('name','nav_display','add_time')
    search_fields = ('name','nav_display')
    list_filter = ('name','nav_display','add_time')
    

class TagAdmin(object):
    '''
        Admin View for Tag
    '''
    list_display = ('name','add_time')
    search_fields = ('name',)
    list_filter = ('name','add_time')
    

class BlogAdmin(object):
    '''
        Admin View for Blog
    '''
    list_display = ('title','excerpt','content','author','tags','category','is_pub','image','fav_nums','click_nums','add_time','update_time')
    search_fields = ('title','excerpt','content','author','tags','category','is_pub','image','fav_nums','click_nums')
    list_filter = ('title','excerpt','content','author__username','tags__name','category__name','is_pub','image','fav_nums','click_nums','add_time','update_time')
    

xadmin.site.register(Category,CategoryAdmin)
xadmin.site.register(Tag,TagAdmin)
xadmin.site.register(Blog,BlogAdmin)