from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from blog.models import Post, Category, BlogComment, Contact
from django.contrib import messages
from django.contrib.auth.models import User
from blog.templatetags import extras
from django.contrib.auth import authenticate, login, logout
from hitcount.views import HitCountDetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from hitcount.models import HitCount
from taggit.models import Tag
from django.db.models import Count


def base(request):
    return render(request, 'base.html')

def home(request):
    popular_posts = Post.objects.filter(section='Popular', status='1').order_by('-id')[0:4]
    recent_posts = Post.objects.filter(status='1').order_by('-time')[0:4]
    latest_posts = Post.objects.filter(status='1').order_by('-time')
    allPosts = Post.objects.filter(status='1')
    cover_post = Post.objects.filter(status='1').order_by('-time')[:1]
    random_posts = Post.objects.filter(status='1').order_by('?')[:3]
    categories = Category.objects.all()
    editors_pick_main = Post.objects.filter(section='Editors_Pick', status='1').order_by('-id')[:1]
    editors_pick = Post.objects.filter(section='Editors_Pick', status='1').order_by('-id')[1:5]
    inspiration_posts = Post.objects.filter(section='Inspiration', status='1').order_by('-time')[:3]
    trending_posts_upper = Post.objects.filter(section='Trending', status='1').order_by('-time')[:1]
    trending_posts_upper_two = Post.objects.filter(section='Trending', status='1').order_by('-time')[1:2]
    trending_posts = Post.objects.filter(section='Trending', status='1').order_by('-time')[2:3]
    trending_posts_two = Post.objects.filter(section='Trending', status='1').order_by('-time')[3:4]
    trending_posts_three = Post.objects.filter(section='Trending', status='1').order_by('-time')[4:5]
    trending_posts_four = Post.objects.filter(section='Trending', status='1').order_by('-time')[5:6]

    paginator = Paginator(latest_posts, 7)
    page = request.GET.get('page')
    try:
        latest_posts = paginator.page(page)
    except PageNotAnInteger:
        latest_posts = paginator.page(1)
    except EmptyPage:
        latest_posts = paginator.page(paginator.num_pages)

    context = {
        'popular_posts': popular_posts,
        'recent_posts': recent_posts,
        'latest_posts': latest_posts,
        'pages': page,
        'allPosts': allPosts,
        'categories': categories,
        'random_posts': random_posts,
        'cover_post': cover_post,
        'editors_pick': editors_pick,
        'editors_pick_main': editors_pick_main,
        'inspiration_posts': inspiration_posts,
        'trending_posts_upper': trending_posts_upper,
        'trending_posts_upper_two': trending_posts_upper_two,
        'trending_posts': trending_posts,
        'trending_posts_two': trending_posts_two,
        "trending_posts_three": trending_posts_three,
        'trending_posts_four': trending_posts_four,
    }
    return render(request, 'home.html', context)


def BlogTags(request, tag_slug=None):
    allPosts = Post.objects.filter(status='1')
    random_posts = Post.objects.filter(status='1').order_by('?')[:3]
    categories = Category.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        allPosts = allPosts.filter(tags__in=[tag])
    allTags = Tag.objects.all()
    context = {
        'allPosts':allPosts, 
        'tag':tag,
        'categories': categories,
        'allTags': allTags,
        'random_posts': random_posts,
    }
    return render(request, 'blog/blogTags.html', context)

def BlogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    categories = Category.objects.all()
    random_posts = Post.objects.filter(status='1').order_by('?')[:3]
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids, status='1').exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags')[:3]

    if post:
        HitCount.objects.get_for_object(post)

    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.id not in replyDict.keys():
            replyDict[reply.parent.id] = [reply]
        else:
            replyDict[reply.parent.id].append(reply)
    context = {
        'post': post, 
        'comments': comments, 
        'user': request.user, 
        'replyDict': replyDict, 
        'categories': categories,
        'random_posts': random_posts,
        'similar_posts':similar_posts,
        }
    return render(request, 'blog/post.html', context)

def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        post = Post.objects.get(id=postSno)
        parentSno = request.POST.get('parentSno')

        # new comment
        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            
        # replies
        else:
            parent = BlogComment.objects.get(id=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
            comment.save()

    return redirect(f'/blog/{post.slug}')

def category_posts(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    random_posts = Post.objects.filter(status='1').order_by('?')[:3]
    categories = Category.objects.all()
    posts = Post.objects.filter(category=category, status='1')
    return render(request, 'blog/category.html', {'category': category, 'posts': posts, 'categories': categories, 'random_posts': random_posts,})

def search(request):
    query = request.GET['query']
    if len(query)>78:
        posts = Post.objects.none()
    else:
        postsTitle = Post.objects.filter(title__icontains=query, status='1')
        postsContent = Post.objects.filter(content__icontains=query, status='1')
        posts = postsTitle.union(postsContent).order_by('-date')
    
    if posts.count() == 0:
        messages.warning(request, 'No search results found. Please refine your query')

    categories = Category.objects.all()
    random_posts = Post.objects.filter(status='1').order_by('?')[:3]
    params = {
        'posts': posts, 
        'query': query, 
        'categories': categories, 
        'random_posts': random_posts,
        }
    return render(request, 'blog/search.html', params)

def Signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        name = request.POST.get('name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        re_pass = request.POST.get('re_pass')

        if pass1!=re_pass:
            return HttpResponse('Password has not matched')
        else:
            myuser = User.objects.create_user(username, email, pass1)
            myuser.save()
            return redirect('/login')
        
    return render(request, 'blog/signup.html')

def Login(request):
    if request.method == 'POST':
        loginusername = request.POST.get('loginusername')
        loginpassword = request.POST.get('loginpassword')
        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'blog/login.html')

def Logout(request):
    logout(request)
    return redirect('home')

def About(request):
    categories = Category.objects.all()
    random_posts = Post.objects.filter(status='1').order_by('?')[:3]
    return render(request, 'about.html', {'categories': categories, 'random_posts': random_posts,})


def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        print(name, email, subject, message)

        if len(name)<2 or len(email)<3 or len(subject)<10 or len(message)<4:
            messages.error(request, 'Please fill the form correctly')
        else:
            contact = Contact(name=name, email=email, subject=subject, message=message)
            contact.save()
            # messages.success(request, 'Your message has been successfully sended.')
    return render(request, 'contact.html')