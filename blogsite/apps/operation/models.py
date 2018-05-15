from django.db import models

from users.models import UserProfile
from blog.models import Blog
# Create your models here.

class BlogComments(models.Model):
    '''
    博客评论
    '''
    user = models.ForeignKey(UserProfile,verbose_name='用户')
    blog = models.ForeignKey(Blog,verbose_name='博客')
    content = models.CharField(max_length=300,verbose_name='评论')
    add_time = models.DateTimeField(auto_now_add=True,verbose_name='回复时间')

    class Meta:
        verbose_name = "博客评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        pass
    

class UserFav(models.Model):
    '''
    用户关注
    '''
    user = models.ForeignKey(UserProfile,verbose_name='用户')
    fav_id = models.IntegerField(default=0,verbose_name='收藏ID')
    fav_type = models.IntegerField(choices=((1,'博客'),(2,'作者')),default=1,verbose_name='收藏类型')
    add_time = models.DateTimeField(auto_now_add=True,verbose_name='收藏时间')

    class Meta:
        verbose_name = "用户关注"
        verbose_name_plural = verbose_name

    def __str__(self):
        pass


class UserMessage(models.Model):
    '''
    用户消息
    '''
    user = models.IntegerField(default=0,verbose_name='接收用户ID')#为0时默认全体发送
    message = models.CharField(max_length=50,verbose_name='消息内容')
    has_read = models.BooleanField(default=False,verbose_name='是否已读')
    add_time = models.DateTimeField(auto_now_add=True,verbose_name='发送时间')

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.message[:10]


class UserBlog(models.Model):
    '''
    用户博客
    '''
    user = models.ForeignKey(UserProfile,verbose_name='作者')
    blog = models.ForeignKey(Blog,verbose_name='作者博客')
    add_time = models.DateTimeField(auto_now_add=True,verbose_name='发表时间')

    class Meta:
        verbose_name = "用户博客"
        verbose_name_plural = verbose_name

    def __str__(self):
        pass
    