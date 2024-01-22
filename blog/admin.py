from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ( "title","author","status","section","date")


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ( "comment", "user", "date")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ( "message", "name", "email")