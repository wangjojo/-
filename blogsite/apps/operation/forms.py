#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-05-15 00:42:34
# @Author  : Wangjojo (wangjojo1995@gmail.com)
from django import forms

from users.models import UserProfile
from blog.models import Blog


class UserImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('image',)
    
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('nick_name','birthday','gender','desc','sign','address','mobile')


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True,min_length=6)
    password2 = forms.CharField(required=True,min_length=6)


class WriteBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title','content','image','category','tags')
    

    
    