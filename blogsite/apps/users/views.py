from django.shortcuts import render
from django.views.generic import View

from blog.models import Blog
# Create your views here.

class IndexView(View):
    '''
    首页
    '''
    def get(self,request):
        blogs = Blog.objects.all()
        return render(request,'index.html',{
            'blogs':blogs,
            })