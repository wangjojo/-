#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-05-14 22:41:22
# @Author  : Wangjojo (wangjojo1995@gmail.com)
from django.conf.urls import url

from .views import *

urlpatterns = [
    #个人信息中心
    url(r'^info/$',UserInfoView.as_view(),name = 'user_info'),
    #修改个人头像
    url(r'^image/upload/$',UserImageView.as_view(),name = 'user_image'),
    #修改个人密码
    url(r'^update/pwd/$',UpdatePwdView.as_view(),name = 'update_pwd'),
    #发送修改邮箱验证码
    url(r'^sendemail_code/$',SendEmailCodeView.as_view(),name = 'sendemail_code'),
    #修改邮箱
    url(r'^update_email/$',UpdateEmailView.as_view(),name = 'update_email'),
    #用户博客
    url(r'^blog/$',UserBlogView.as_view(),name = 'user_blog'),
    #fav作者
    url(r'^myauthor/$',FavAuthorView.as_view(),name = 'fav_author'),
    #fav博客
    url(r'^myblog/$',FavBlogView.as_view(),name = 'fav_blog'),
    #用户消息
    url(r'^message/$',UserMessageView.as_view(),name = 'user_message'),   
    #系统消息
    url(r'^message_all/$',UserMessageAllView.as_view(),name = 'user_message_all'),  
    #添加收藏
    url(r'^add_fav/$',AddFavView.as_view(),name = 'add_fav'),
]