from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post,Category,Tag
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
import markdown
import re
from blog.custom_paginator import CustomPaginator
from django.core.paginator import EmptyPage, PageNotAnInteger


def index(request):
    post_list = Post.objects.all()
    return render(request, 'index.html', context={'post_list': post_list})


def listView(request):
    post_list = Post.objects.all()

    current_page = request.GET.get("page", '1')
    paginator = CustomPaginator(current_page, 9, post_list, 3)
    try:
        paginator = paginator.page(current_page)  # 获取前端传过来显示当前页的数据
    except PageNotAnInteger:
        # 如果有异常则显示第一页
        paginator = paginator.page(1)
    except EmptyPage:
        # 如果没有得到具体的分页内容的话,则显示最后一页
        paginator = paginator.page(paginator.num_pages)
    return render(request, 'list.html', {"paginator": paginator})


def aboutView(request):
    post_list = Post.objects.all()
    return render(request, 'about.html', context={'post_list': post_list})


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    md =markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        TocExtension(slugify=slugify),
    ])
    post.body=md.convert(post.body)

    m=re.search('<div class="toc">\s*<ul>(.*)</ul>\s*</div>',md.toc,re.S)
    post.toc=m.group(1) if m is not None else ''
    return render(request, 'blog-light.html', context={'post': post})

def archive(request,year,month):
    post_list=Post.objects.filter(created_time__year=year,
                                  created_time__month=month
                                  ).order_by('-created_time')

    current_page = request.GET.get("page", '1')
    paginator = CustomPaginator(current_page, 9, post_list, 10)
    try:
        paginator = paginator.page(current_page)  # 获取前端传过来显示当前页的数据
    except PageNotAnInteger:
        # 如果有异常则显示第一页
        paginator = paginator.page(1)
    except EmptyPage:
        # 如果没有得到具体的分页内容的话,则显示最后一页
        paginator = paginator.page(paginator.num_pages)

    return render(request,'list.html',context={'paginator':paginator})

def category(request,pk):
    cate=get_object_or_404(Category,pk=pk)
    post_list=Post.objects.filter(category=cate).order_by('-created_time')

    current_page = request.GET.get("page", '1')
    paginator = CustomPaginator(current_page, 9, post_list, 10)
    try:
        paginator = paginator.page(current_page)  # 获取前端传过来显示当前页的数据
    except PageNotAnInteger:
        # 如果有异常则显示第一页
        paginator = paginator.page(1)
    except EmptyPage:
        # 如果没有得到具体的分页内容的话,则显示最后一页
        paginator = paginator.page(paginator.num_pages)

    return render(request,'list.html',context={'paginator':paginator})

def tag(request,pk):
    t=get_object_or_404(Tag,pk=pk)
    post_list=Post.objects.filter(tags=t).order_by('-created_time')
    current_page = request.GET.get("page", '1')
    paginator = CustomPaginator(current_page, 9, post_list, 10)
    try:
        paginator = paginator.page(current_page)  # 获取前端传过来显示当前页的数据
    except PageNotAnInteger:
        # 如果有异常则显示第一页
        paginator = paginator.page(1)
    except EmptyPage:
        # 如果没有得到具体的分页内容的话,则显示最后一页
        paginator = paginator.page(paginator.num_pages)

    return render(request,'list.html',context={'paginator':paginator})