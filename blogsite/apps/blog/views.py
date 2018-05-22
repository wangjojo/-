from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.db.models import Q

from .models import Category,Blog,Tag
from users.models import UserProfile
from operation.models import UserFav,BlogComments
from utils.pagination import paging
# Create your views here.

class BlogDetailView(View):
    '''
    博客详情
    '''
    def get(self,request,blog_id):
        blog = Blog.objects.get(id = blog_id)
        #增加点击
        blog.click_nums += 1
        blog.save()

        tags = blog.tags.all()

        #检查是否关注了博客和作者

        author_has_fav = False
        blog_has_fav = False
        
        if request.user.is_authenticated():
            if UserFav.objects.filter(user = request.user,fav_id=blog_id,fav_type=1):
                blog_has_fav = True

            if UserFav.objects.filter(user = request.user,fav_id=blog.author.id,fav_type=2):
                author_has_fav = True

        #查询博客评论
        all_comments = BlogComments.objects.filter(blog = blog)
        comment_nums = all_comments.count()

        return render(request,'blog_detail.html',{
            'blog':blog,
            'tags':tags,
            'blog_has_fav':blog_has_fav,
            'author_has_fav':author_has_fav,
            'all_comments':all_comments,
            'comment_nums':comment_nums,
            })


class BlogCategoryView(View):
    '''
    博客分类详情
    '''
    def get(self,request,category_id):
        category = Category.objects.get(id = category_id)
        all_blogs = category.blog_set.all()

        blogs = paging(all_blogs,request = request)

        return render(request,'blog_category.html',{
            'category':category,
            'all_blogs':blogs,
            })


class BlogAuthorView(View):
    '''
    博客作者详情
    '''
    def get(self,request,author_id):
        author = UserProfile.objects.get(id = author_id)
        author.click_nums += 1
        author.save()

        all_blogs = author.blog_set.all()

        #是否收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFav.objects.filter(user = request.user,fav_id = author_id,fav_type = 2):
                has_fav = True

        blogs = paging(all_blogs,request = request,nums = 5)

        return render(request,'blog_author_detail.html',{
            'author':author,
            'all_blogs':blogs,
            'has_fav':has_fav,
            })

class ArchivesView(View):
    '''
    归档
    '''
    def get(self,request,year,month):
        all_blogs = Blog.objects.filter(add_time__year = year,add_time__month = month).order_by('-add_time')

        blogs = paging(all_blogs,request = request)

        return render(request,'blog_archives.html',{
            'all_blogs':blogs,
            'year':year,
            'month':month,
            })


class BlogTagView(View):
    '''
    标签云
    '''
    def get(self,request,tag_id):
        tag = Tag.objects.get(id = tag_id)
        all_blogs = tag.blog_set.all().order_by('-add_time')

        blogs = paging(all_blogs,request = request)

        return render(request,'blog_tag.html',{
            'all_blogs':blogs,
            'tag':tag,
            })


class AddCommentView(View):
    '''
    添加评论
    '''
    def post(self,request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}',content_type = 'application/json')

        blog_id = int(request.POST.get('blog_id'),0)
        comments = request.POST.get('comments','')

        if blog_id > 0 and comments:
            blog = Blog.objects.get(id = blog_id)

            blog_comment = BlogComments()
            blog_comment.user = request.user
            blog_comment.blog = blog
            blog_comment.content = comments
            blog_comment.save()
            return HttpResponse('{"status":"success","msg":"评论成功"}',content_type = 'application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"评论出错"}',content_type = 'application/json')


class SearchView(View):
    '''
    全局搜索
    ''' 
    def get(self,request):
        if request.GET.get('type') == 'blog':
            all_blogs = Blog.objects.all()
            keywords = request.GET.get('keywords','')
            if keywords:
                all_results = all_blogs.filter(Q(title__icontains = keywords)|Q(content__icontains = keywords)|Q(want_to_say__icontains = keywords)).order_by('add_time')

                results = paging(all_results,request = request,nums = 4)

                return render(request,'search.html',{
                    'name': 'blog',
                    'all_results': results,
                    })

        elif request.GET.get('type') == 'author':
            all_authors = UserProfile.objects.all()
            keywords = request.GET.get('keywords','')
            if keywords:
                all_results = all_authors.filter(Q(nick_name__icontains = keywords)|Q(desc__icontains = keywords)|Q(sign__icontains = keywords))

                results = paging(all_results,request = request,nums = 4)

                return render(request,'search.html',{
                    'name': 'author',
                    'all_results': results,
                    })            