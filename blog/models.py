from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from taggit.managers import TaggableManager
from django.utils.timezone import now
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from hitcount.models import HitCountMixin, HitCount

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class Post(models.Model, HitCountMixin):
    STATUS = (
        ('0', 'Draft'),
        ('1', 'Publish')
    )

    SECTION = (
        ('Popular', 'Popular'),
        ('Editors_Pick', 'Editors_Pick'),
        ('Trending', 'Trending'),
        ('Inspiration', 'Inspiration'),
    )
    
    title = models.CharField(max_length=255)
    content = RichTextUploadingField()
    thumbnail = models.ImageField(upload_to='featured_image/%Y/%m/%d/') 
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = TaggableManager()
    author = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS, max_length=150)
    section = models.CharField(choices=SECTION, max_length=255)

    def __str__(self):
        return self.title + ' by ' + self.author

class BlogComment(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    date = models.DateField(default=now)
    def __str__(self):
        return self.comment[0:13] + "..." + "by " + self.user.username
    
class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    subject = models.TextField()
    email = models.CharField(max_length=255)
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return 'Message from ' + self.name + ' - ' + self.email