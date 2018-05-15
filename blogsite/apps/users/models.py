from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class UserProfile(AbstractUser):
    nick_name = models.CharField(blank=True, max_length=50,verbose_name='昵称')
    birthday = models.DateField(null=True,blank=True,verbose_name='生日')
    gender = models.CharField(choices=(('male','男'),('female','女')),default='male',max_length=10,verbose_name='性别')
    desc = models.CharField(max_length=300,blank=True,verbose_name='个人简介')
    sign = models.CharField(blank=True, max_length=80,verbose_name='个性签名')
    address = models.CharField(blank=True, max_length=100,verbose_name='地址')
    mobile = models.CharField(null=True,blank=True,max_length=11,verbose_name='手机号码')
    image = models.ImageField(upload_to='images/user/%Y/%m',default='images/user_default.png',blank=True,max_length=100,verbose_name='头像')
    fav_nums = models.IntegerField(default=0,verbose_name='收藏数')
    click_nums = models.IntegerField(default=0,verbose_name='点击数')

    class Meta:
        verbose_name='用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    '''
    邮箱验证码
    '''
    code = models.CharField(max_length=50,verbose_name='验证码')
    email = models.EmailField(max_length=50,verbose_name='邮箱')
    send_type = models.CharField(choices=(('register','注册'),('forget','忘记密码'),('update_email','修改邮箱')),
        default='register',max_length=20,verbose_name='发送类型')
    send_time = models.DateTimeField(auto_now_add=True,verbose_name="发送时间")

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.email,self.send_type)
    

class Banner(models.Model):
    '''
    轮播图
    '''
    title = models.CharField(max_length=50,verbose_name='轮播图')
    image = models.ImageField(upload_to='images/banner/%Y/%m',max_length=100,blank=True,verbose_name='图片')
    index = models.IntegerField(default=100,verbose_name='排序')
    url = models.URLField(max_length=100,verbose_name="访问地址")
    add_time = models.DateTimeField(auto_now_add=True,verbose_name='添加时间')


    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title