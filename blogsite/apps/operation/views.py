import json

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password

from utils.mixin_untils import LoginRequiredMixin
from utils.email_send import send_user_email
from utils.pagination import paging
from .forms import *
from users.models import UserProfile,EmailVerifyRecord
from blog.models import Blog,Category,Tag
from .models import UserFav,UserMessage

# Create your views here.
class AddFavView(View):
    def post(self,request):
        fav_id = int(request.POST.get('fav_id',0))
        fav_type = int(request.POST.get('fav_type',0))

        #检查用户是否登录
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}',content_type = 'application/json')

        exist_record = UserFav.objects.filter(user = request.user,fav_id = fav_id,fav_type = fav_type)
        #如果记录存在视为取消收藏,并减少收藏数
        if exist_record:
            exist_record.delete()
            if fav_type == 1:
                blog = Blog.objects.get(id = fav_id)
                blog.fav_nums -= 1
                if blog.fav_nums < 0:
                    blog.fav_nums = 0
                blog.save()

            elif fav_type == 2:
                author = UserProfile.objects.get(id = fav_id)
                author.fav_nums -= 1
                if author.fav_nums < 0:
                    author.fav_nums = 0
                author.save()

            return HttpResponse('{"status":"success","msg":"取消收藏成功"}',content_type = 'application/json')
        else:
            user_fav = UserFav()
            if fav_id > 0 and fav_type > 0:
                user_fav.user = request.user
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.save()

                if fav_type == 1:
                    blog = Blog.objects.get(id = fav_id)
                    blog.fav_nums += 1
                    blog.save()

                elif fav_type == 2:
                    author = UserProfile.objects.get(id = fav_id)
                    author.fav_nums += 1
                    author.save()

                return HttpResponse('{"status":"success","msg":"收藏成功"}',content_type = 'application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"收藏出错"}',content_type = 'application/json')



class UserInfoView(LoginRequiredMixin,View):
    '''
    用户信息中心
    '''
    def get(self,request):
        return render(request,'usercenter.html',{})

    def post(self,request):
        user_form = UserInfoForm(request.POST,instance = request.user)
        print('a')
        if user_form.is_valid():
            request.user.save()
            print('b')
            return HttpResponse('{"status":"success","msg":"修改成功"}',content_type = 'application/json')
        else:
            print('c')
            return HttpResponse(json.dumps(user_form.errors),content_type = 'application/json')

class UserImageView(LoginRequiredMixin,View):
    '''
    用户修改头像
    '''
    def post(self,request):
        user_image = UserImageForm(request.POST,request.FILES,instance=request.user)
        if user_image.is_valid():
            request.user.save()

            return HttpResponse('{"status":"success","msg":"修改成功"}',content_type = 'application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"修改失败"}',content_type = 'application/json')


class UpdatePwdView(LoginRequiredMixin,View):
    '''
    用户修改密码
    '''
    def post(self,request):
        pwd_form = ModifyPwdForm(request.POST)

        if pwd_form.is_valid():
            password1 = pwd_form.cleaned_data['password1']
            password2 = pwd_form.cleaned_data['password2']

            if password1 == password2:
                user = request.user
                user.password = make_password(password1)
                user.save()

                return HttpResponse('{"status":"success","msg":"修改成功"}',content_type = 'application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"两次密码不一致"}',content_type = 'application/json')
        else:
            return HttpResponse(json.dumps(pwd_form.errors),content_type = 'application/json')


class SendEmailCodeView(LoginRequiredMixin,View):
    '''
    用户修改邮箱验证码
    '''
    def get(self,request):
        email = request.GET.get('email','')
        if UserProfile.objects.filter(email = email):
            return HttpResponse('{"email":"邮箱已经注册"}',content_type = 'application/json')

        send_user_email(email = email,send_type='update_email')
        return HttpResponse('{"status":"success","msg":"邮件发送成功"}',content_type = 'application/json')


class UpdateEmailView(LoginRequiredMixin,View):
    '''
    用户修改邮箱
    '''
    def post(self,request):
        email = request.POST.get('email','')
        code = request.POST.get('code','')

        record = EmailVerifyRecord.objects.filter(code = code)
        
        if record:
            request.user.email = email
            request.user.save()

            return HttpResponse('{"status":"success","msg":"修改成功"}',content_type = 'application/json')
        else:
            return HttpResponse('{"email":"验证码失效"}',content_type = 'application/json')


class UserBlogView(LoginRequiredMixin,View):
    '''
    用户博客
    '''
    def get(self,request):
        all_blogs = Blog.objects.filter(author = request.user)

        sort = request.GET.get('sort','')

        if sort == 'add_time':
            all_blogs = all_blogs.order_by('-add_time')
        elif sort == 'click':
            all_blogs = all_blogs.order_by('-click_nums')
        elif sort == 'fav':
            all_blogs = all_blogs.order_by('-fav_nums')

        blogs = paging(all_blogs,request = request)
 
        return render(request,'usercenter_myblog.html',{
            'all_blogs':blogs,
            })


class FavAuthorView(LoginRequiredMixin,View):
    '''
    fav用户
    '''
    def get(self,request):
        #取出关注作者记录
        records = UserFav.objects.filter(user=request.user,fav_type= 2)
        #取出作者id
        id_list = [each.fav_id for each in records]
        #取出关注作者
        all_authors = UserProfile.objects.filter(id__in = id_list)

        authors = paging(all_authors,request = request,nums = 5)

        return render(request,'usercenter_fav_author.html',{
            'all_authors':authors,
            })


class FavBlogView(LoginRequiredMixin,View):
    '''
    fav博客
    '''
    def get(self,request):
        #取出关注博客记录
        records = UserFav.objects.filter(user=request.user,fav_type= 1)
        #取出博客id
        id_list = [each.fav_id for each in records]
 
        #取出关注作者
        all_blogs = Blog.objects.filter(id__in = id_list)

        blogs = paging(all_blogs,request = request)

        return render(request,'usercenter_fav_blog.html',{
            'all_blogs':blogs,
            })


class UserMessageView(LoginRequiredMixin,View):
    '''
    用户消息
    '''    
    def get(self,request):
        all_messages = UserMessage.objects.filter(user = request.user.id)

        for message in all_messages:
            message.has_read = True
            message.save()

        #针对单条消息的已读还没做

        return render(request,'usercenter_message.html',{
            'all_messages':all_messages,
            })


class UserMessageAllView(LoginRequiredMixin,View):
    '''
    系统消息
    '''    
    def get(self,request):
        all_messages = UserMessage.objects.filter(user = 0)

        for message in all_messages:
            message.has_read = True
            message.save()

        return render(request,'usercenter_message_all.html',{
            'all_messages':all_messages,
            })


class WriteBlogView(LoginRequiredMixin,View):
    def get(self,request):
        categorys = Category.objects.filter(is_admin = False)
        tags = Tag.objects.all()

        return render(request,'usercenter_writeblog.html',{
            'categorys':categorys,
            'tags':tags,
            })

    def post(self,request):
        blog_form = WriteBlogForm(request.POST)
        if blog_form.is_valid():    
            title = blog_form.cleaned_data['title']
            content = blog_form.cleaned_data['content']
            say = blog_form.cleaned_data['say']
            category = blog_form.cleaned_data['category']
            tag = blog_form.cleaned_data['tag']
            image = blog_form.cleaned_data['image']

        blog = Blog()
        blog.title = title
        blog.content = content
        #获取分类
        category = Category.objects.get(name = category)
        blog.category = category
        #获取封面
        if image:
            blog.image = image
        #获取作者想说的话,如果为空，则填入作者的个性签名
        if not say:
            blog.want_to_say = request.user.sign
        else:
            blog.want_to_say = say

        blog.author = request.user
        blog.save()
        #获取标签
        if tag:
            tag_list = tag.split(',')
            for tag in tag_list:
                tag = Tag.objects.get(name = tag)
                blog.tags.add(tag)

        blog.save()


        print('ok')

        return HttpResponse('{"status":"success","msg":"发布成功"}',content_type = 'application/json')
