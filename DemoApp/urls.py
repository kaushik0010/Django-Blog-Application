"""
URL configuration for NewBlog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('postComment', views.postComment, name='postComment'),
    path('', views.home, name='home'),
    path('blog/<str:slug>', views.BlogPost, name='BlogPost'),
    path('search', views.search, name='search'),
    path('signup', views.Signup, name='Signup'),
    path('about', views.About, name='About'),
    path('contact', views.contact, name='contact'),
    path('login', views.Login, name='Login'),
    path('logout', views.Logout, name='Logout'),
    path('category/<str:category_name>/', views.category_posts, name='category_posts'),
    path('tag/<slug:tag_slug>/', views.BlogTags, name='BlogTags'),
    path('ckeditor/',include('ckeditor_uploader.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
