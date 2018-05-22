#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-05-18 01:59:43
# @Author  : Wangjojo (wangjojo1995@gmail.com)
from django import template
from django.db.models.aggregates import Count

from ..models import Blog,Tag

register = template.Library()

@register.simple_tag
def archives():
    return Blog.objects.dates('add_time','month',order = 'DESC')

@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_blogs=Count('blog')).filter(num_blogs__gt = 0)

@register.simple_tag
def get_hot_blogs():
    return Blog.objects.all().order_by('-click_nums')[:5]