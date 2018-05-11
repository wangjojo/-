#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-05-11 13:28:56
# @Author  : Wangjojo (wangjojo1995@gmail.com)
from .models import *

import xadmin
from xadmin import views

class BaseSetting(object):
    '''
    '''
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = 'jojo的管理系统'
    site_footer = 'jojo在线'

    menu_style = 'accordion'


class EmailVerifyRecordAdmin(object):
    list_display = ['code','email','send_type','send_time']
    search_fields = ['code','email','send_type']
    list_filter = ['code','email','send_type','send_time']


class BannerAdmin(object):
    list_display = ['index','title','image','url','add_time']
    search_fields = ['index','title','image','url']
    list_filter = ['index','title','image','url','add_time']


xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)
xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)