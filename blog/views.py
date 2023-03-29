from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse,reverse_lazy
from django.views.generic import ListView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import CommentForm,CreatePostForm
from datetime import date
from blog.models import *
# Create your views here.

all_posts = []


# Create your views here.


class StartingPage(ListView):
    model=Post
    template_name='blog/index.html'
    context_object_name="posts"
    ordering=["-date"]

    def get_queryset(self):
        queryset=super().get_queryset()
        data=queryset[:3]
        return data
         
class AllPosts(ListView):
    model=Post
    template_name='blog/all-posts.html'
    context_object_name="all_posts"


class DetailPosts(View):
    
    def get(self,request,slug):
        if request.user.is_authenticated:
            post=Post.objects.get(slug=slug)
            already_liked=Likes.objects.filter(post=post,user=request.user)
            all_comments=Comment.objects.filter(post=post)
            if already_liked:
                liked=True
            else:
                liked=False
            context={
                'post_tags':post.tags.all(),
                'post':post,
                'comment_form':CommentForm(),
                'liked':liked,
                'comments':all_comments

            }
            return render(request,'blog/post-detail.html',context)
        else:
            return redirect(reverse_lazy('login'))

    def post(self,request,slug):
        post=Post.objects.get(slug=slug)
        comment_form=CommentForm(request.POST)
        user=request.user
       
        if comment_form.is_valid():
            if request.POST['user_email'] == User.objects.get(email=user.email).email:
                comment=comment_form.save(commit=False)
                comment.post=post
                comment.save()
                messages.success(request,"comment saved successfully")
                return HttpResponseRedirect(reverse_lazy('post-detail-page',args=[slug]))
        context={
            'post_tags':post.tags.all(),
            'post':post,
            'comment_form':comment_form,
            'msg':'comment allowed for logged in  user only'

        }
        return render(request,'blog/post-detail.html',context)


def liked(request,slug):
    post=Post.objects.get(slug=slug)
    user=request.user
    already_liked=Likes.objects.filter(post=post,user=user)
    print(already_liked)
    if not already_liked:
        Liked_post=Likes(post=post,user=user)
        Liked_post.save()
    return HttpResponseRedirect(reverse('post-detail-page',args=[slug]))
    
def unliked(request,slug):
    post=Post.objects.get(slug=slug)
    user=request.user
    already_liked=Likes.objects.filter(post=post,user=user)
    already_liked.delete()
    return HttpResponseRedirect(reverse('post-detail-page',args=[slug]))

class ReadLaterView(View):
    def get(self,request):
        stored_post=request.session.get("stored_post")

        context={}
        if stored_post is None or len(stored_post)==0:
            context['posts']='No post to show'
            context['has_posts']=False
        else:
            post=Post.objects.filter(id__in=stored_post)
            context['posts']=post
            context['has_posts']=True

        return render(request,'blog/read-later.html',context)

    def post(self,request):
        stored_post=request.session.get("stored_post")

        if stored_post is None:
            stored_post=[]
        post_id=request.POST.get("post_id")
        stored_post.append(int(post_id))
        request.session['stored_post']=stored_post
        return HttpResponseRedirect('/')
    
@login_required(login_url="login")
def create_post(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            fm=CreatePostForm(request.POST,request.FILES)
            if fm.is_valid():
                form=fm.save(commit=False)
                title=form.title
                form.slug=title.replace(" ","-")
                messages.success(request,"Post Created Successfully")
                form.save()
                return HttpResponseRedirect(reverse('starting-page'))
        else:
            fm=CreatePostForm()
    return render(request,'blog/create-post.html',{'form':fm})
    