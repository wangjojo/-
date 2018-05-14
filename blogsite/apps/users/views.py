from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.hashers import make_password

from blog.models import Blog
from .forms import *
from .models import UserProfile,EmailVerifyRecord
from utils.email_send import send_user_email
# Create your views here.

class CustomBackend(ModelBackend):
    '''
    拓展authenticate方法,可以通过邮箱或用户名登录
    '''
    def authenticate(self,username = None,password = None,**kwargs):
        try:
            user = UserProfile.objects.get(Q(username = username)|Q(email = username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class IndexView(View):
    '''
    首页
    '''
    def get(self,request):
        blogs = Blog.objects.all()
        return render(request,'index.html',{
            'blogs':blogs,
            })


class LoginView(View):
    '''
    登录视图
    '''
    def get(self,request):
        return render(request,'login.html',{
            })

    def post(self,request):
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            #验证用户是否存在

            user = authenticate(username = username,password = password)

            if user is not None: 
                if user.is_active:
                    login(request,user)
                    return redirect(reverse('index'))
                else:
                    return render(request,'login.html',{
                        'login_form':login_form,
                        'msg':'用户未激活'
                        })
            else:
                return render(request,'login.html',{
                    'msg':'用户名或密码输入错误',
                    'login_form':login_form,
                    })
        else:
            return render(request,'login.html',{
                'login_form':login_form,
                'msg':'用户名或密码输入错误',
                })


class LogoutView(View):
    '''
    登出
    '''
    def get(self,request):
        logout(request)
        return redirect(reverse('index'))


class RegisterView(View):
    '''
    注册
    '''
    def get(self,request):
        register_form = RegisterForm()
        return render(request,'register2.html',{
            'register_form':register_form,
            })

    def post(self,request):
        register_form = RegisterForm(request.POST)
        #验证数据
        if register_form.is_valid():
            #检查用户是否存在
            email = request.POST.get('email','')
            password = request.POST.get('password')

            if UserProfile.objects.filter(email = email):
                return render(request,'register2.html',{
                    'register_form':register_form,
                    'msg':'用户已经存在',
                    })
            else:
                #保存用户
                user_profile = UserProfile()
                user_profile.is_active = False
                user_profile.username = email
                user_profile.email = email
                user_profile.password = make_password(password)
                user_profile.save()
                #发送激活邮件
                send_user_email(email,send_type = 'register')

                return render(request,'register2.html',{
                    'msg':'注册成功,激活邮件已发送,请登录邮箱激活账号'
                    })
        else:
            return render(request,'register2.html',{
                'register_form':register_form,
                })


class ActiveUserView(View):
    '''
    激活用户
    '''
    def get(self,requset,email_code):
        #查看是否有发送记录
        all_codes = EmailVerifyRecord.objects.filter(code = email_code)

        if all_codes is not None:
            for each in all_codes:
                email = each.email           
                user = UserProfile.objects.get(email = email)
                user.is_active = True
                user.save()

            return redirect(reverse('login'))
        else:
            return render(request,'active_fail.html')


class ForgetPwdView(View):
    '''
    忘记密码
    '''
    def get(self,request):
        forget_form = ForgetPwdForm()

        return render(request,'forget.html',{
            'forget_form':forget_form,
            })

    def post(self,request):
        forget_form = ForgetPwdForm(request.POST)

        if forget_form.is_valid():
            email = request.POST.get('email')

            #验证用户是否存在
            if UserProfile.objects.filter(email = email):
                send_user_email(email = email,send_type = 'forget')

                return render(request,'forget.html',{'msg':'重置密码链接已发送,请查收'})
            else:
                return render(request,'forget.html',{'msg':'用户不存在','forget_form':forget_form})
        else:
            return render(request,'forget.html',{'msg':'用户不存在','forget_form':forget_form})


class ResetView(View):
    '''
    重置密码链接
    '''
    def get(self,request,reset_code):
        all_codes = EmailVerifyRecord.objects.filter(code = reset_code)

        if all_codes:
            for code in all_codes:
                email = code.email
                return render(request,'reset_pwd.html',{
                    'email':email,
                    })
        else:
            return render(request,'forget.html',{'msg':'链接失效，请重试'})


class ResetPwdView(View):
    '''
    重置密码
    '''
    def post(self,request):
        reset_form = ResetPwdForm(request.POST)

        if reset_form.is_valid():
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            email = request.POST.get('email')

            if password1 == password2:
                user = UserProfile.objects.get(email = email)
                user.password = make_password(password1)
                user.save()

                return render(request,'login.html',{'msg':'密码修改成功，请登录'})

            else:
                return render(request,'reset_pwd.html',{
                    'email':email,
                    'msg':'两次密码不一致，请修改'
                    })
        else:
            email = request.POST.get('email')
            return render(request,'reset_pwd.html',{
                'email':email,
                'msg':'输入错误'
                })