from datetime import datetime

from django.db import models

from users.models import UserProfile
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20,verbose_name='类别')
    nav_display = models.BooleanField(default=True,verbose_name='是否导航显示')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=20,verbose_name='标签')
    add_time = models.DateTimeField(auto_now_add=True,verbose_name='添加时间')
    
    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=50,verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    excerpt = models.CharField(blank=True, max_length=100,verbose_name='摘要')
    is_pub = models.BooleanField(default=True,verbose_name='是否发表')
    add_time = models.DateTimeField(auto_now_add=True,editable=True,verbose_name='发表时间')
    update_time = models.DateTimeField(auto_now=True,null=True,verbose_name='更新时间')
    image = models.ImageField(upload_to='images/blog/%Y/%m',default='images/blog_default.png',blank=True,max_length=100,verbose_name='封面')
    fav_nums = models.IntegerField(default=0,verbose_name='收藏数')
    click_nums = models.IntegerField(default=0,verbose_name='点击数')

    category = models.ForeignKey(Category,verbose_name='分类')
    tags = models.ManyToManyField(Tag,blank=True,verbose_name='标签')
    author = models.ForeignKey(UserProfile,verbose_name='作者')

    class Meta:
        verbose_name = "博客"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title