from django.shortcuts import render
from django.views.generic import View

from .models import Category,Blog,Tag
from users.models import UserProfile
from operation.models import UserFav
# Create your views here.

class BlogDetailView(View):
    '''
    博客详情
    '''
    def get(self,request,blog_id):
        blog = Blog.objects.get(id = blog_id)
        tags = blog.tags.all()

        #检查是否关注了博客和作者

        author_has_fav = False
        blog_has_fav = False
        
        if request.user.is_authenticated():
            if UserFav.objects.filter(user = request.user,fav_id=blog_id,fav_type=1):
                blog_has_fav = True

            if UserFav.objects.filter(user = request.user,fav_id=blog.author.id,fav_type=2):
                author_has_fav = True


        return render(request,'blog_detail.html',{
            'blog':blog,
            'tags':tags,
            'blog_has_fav':blog_has_fav,
            'author_has_fav':author_has_fav,
            })


class BlogCategoryView(View):
    '''
    博客分类详情
    '''
    def get(self,request,category_id):
        category = Category.objects.get(id = category_id)
        blogs = category.blog_set.all()
        return render(request,'blog_category.html',{
            'category':category,
            'blogs':blogs,
            })


class BlogAuthorView(View):
    '''
    博客作者详情
    '''
    def get(self,request,author_id):
        author = UserProfile.objects.get(id = author_id)
        all_blogs = author.blog_set.all()

        #是否收藏
        has_fav = False
        if UserFav.objects.filter(user = request.user,fav_id = author_id,fav_type = 2):
            has_fav = True


        return render(request,'blog_author_detail.html',{
            'author':author,
            'all_blogs':all_blogs,
            'has_fav':has_fav,
            })
