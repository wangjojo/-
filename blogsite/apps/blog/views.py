from django.shortcuts import render
from django.views.generic import View

from .models import Category,Blog,Tag
# Create your views here.

class BlogDetailView(View):
    '''
    博客详情
    '''
    def get(self,request,blog_id):
        blog = Blog.objects.get(id = blog_id)
        tags = blog.tags.all()
        return render(request,'blog_detail.html',{
            'blog':blog,
            'tags':tags,
            })


class BlogCategoryView(View):
    '''
    博客详情
    '''
    def get(self,request,category_id):
        category = Category.objects.get(id = category_id)
        blogs = category.blog_set.all()
        return render(request,'blog_category.html',{
            'category':category,
            'blogs':blogs,
            })