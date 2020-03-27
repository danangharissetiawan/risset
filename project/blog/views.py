from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from taggit.models import Tag

from .models import Post, Comment, Like, DisLike, Kategori
from .forms import CommentForm

class AllPost(ListView):
    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'posts'
    ordering = '-created'
    # paginate_by = 10

    def get_context_data(self, **kwargs):
        kategori_list = Kategori.objects.all()
        self.kwargs.update({'kategori_list':kategori_list})

        user = self.request.user
        self.kwargs.update({'users':user})


        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        context["title"] = "Blog"
        context["active"] = "active"
        return context


class PostListView(ListView):
    model = Post
    template_name = "blog/blog.html"
    context_object_name = 'posts'
    ordering = "-created"
    # paginate_by = 10

    def get_queryset(self):
        b = Kategori.objects.get(kategori=self.kwargs['kategori'])
        self.queryset = b.kategoris.all()
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        kategori_list = Kategori.objects.all().exclude(kategori=self.kwargs['kategori'])
        self.kwargs.update({'kategori_list':kategori_list})

        kategori_active = Kategori.objects.get(kategori=self.kwargs['kategori'])
        self.kwargs.update({'kategori_active':kategori_active})
        print(kategori_active)

        user = self.request.user
        self.kwargs.update({'users':user})


        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        context["title"] = kategori_active
        context["active"] = "active"
        return context


class Tags(ListView):
    # model = Post
    template_name = "blog/blog.html"
    context_object_name = 'posts'
    # ordering = '-created'
    # paginate_by = 10

    def get_queryset(self):
        self.queryset = Post.objects.filter(tags__name__contains=self.kwargs['tag'])
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        kategori_list = Kategori.objects.all()
        self.kwargs.update({'kategori_list':kategori_list})

        user = self.request.user
        self.kwargs.update({'users':user})

        kategori_active = Tag.objects.get(name=self.kwargs['tag'])
        self.kwargs.update({'kategori_active':kategori_active})

        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        context["title"] = kategori_active
        context["active"] = "active"
        return context


def search(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        submitbutton = request.GET.get('submit')
        if query is not None:
            lookups = Q(judul__icontains=query) | Q(
                tags__name__icontains=query) | Q(kategori__kategori__icontains=query) | Q(slug__icontains=query) | Q(user__username__icontains=query)

            posts = Post.objects.filter(lookups).distinct()
            kategori_list = Kategori.objects.all()

            context = {
                'posts': posts,
                'submitbutton': submitbutton,
                'kategori_list':kategori_list,
                'title':'Search',
                'kategori_active': 'Search'
            }
            return render(request, 'blog/search.html', context)
        else:
            return render(request, 'blog/search.html')
    else:
        return render(request, 'blog/search.html')
    


class PostDetailView(View):
    model = Post
    template_name = "blog/detail.html"
    comment_form = CommentForm()
    is_bookmarks = False
    is_archives = False


    def get(self, *args, **kwargs):
        post = self.model.objects.get(slug=self.kwargs['slug'])
        post.views = post.views+1
        post.save()

        if post.bookmarks.filter(id=self.request.user.id):
            self.is_bookmarks = True;


        comments = post.comments.filter(activate=True, reply=None).order_by('-created')
        j_comments = post.comments.filter().order_by('-created')

        self.context = {
            'post':post,
            'comment_form':self.comment_form,
            'is_bookmarks': self.is_bookmarks,
            'comments':comments,
            'jumlah_comment': j_comments,
            'title':post,
        }
        return render(self.request, self.template_name, self.context)

class Comment(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'
    model = Comment

    def post(self, *args, **kwargs):
        post = Post.objects.get(slug=kwargs['slug'])
        comments = self.model.objects.filter(activate=True, reply=None).order_by('-created')
        if self.request.method == 'POST':
            self.comment_form = CommentForm(self.request.POST or None)
            if self.comment_form.is_valid():
                new_comment = self.comment_form.save(commit=False)
                reply_id = self.request.POST.get('reply')
                comment_qs = None
                if reply_id:
                    comment_qs = post.comments.get(id=reply_id)
                new_comment.reply = comment_qs
                new_comment.user = self.request.user
                new_comment.post = post
                new_comment.save()
                messages.success(self.request, "Komentar terkirin! sedang menunggu moderasi")
        return redirect('blog:detail', kwargs['slug'])


class LikeDislike(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        # p = Post.objects.get(slug=kwargs['slug'])
        # print(p)
        post_id = self.kwargs.get('post_id', None)
        opinion = self.kwargs.get('opinion', None) #like atau dislike

        post = get_object_or_404(Post, id=post_id)

        try:
            post.dis_likes
        except Post.dis_likes.RelatedObjectDoesNotExist as identifier:
            DisLike.objects.create(post=post)

        try:
            post.likes
        except Post.likes.RelatedObjectDoesNotExist as identifier:
            Like.objects.create(post=post)

        if opinion.lower() == 'like':
            if request.user in post.likes.users.all():
                post.likes.users.remove(request.user)
            else:
                post.likes.users.add(request.user)
                post.dis_likes.users.remove(request.user)
        elif opinion.lower() == 'dis_like':
            if request.user in post.dis_likes.users.all():
                post.dis_likes.users.remove(request.user)
            else:
                post.dis_likes.users.add(request.user)
                post.likes.users.remove(request.user)
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def bookmarks(request, id):
    post = get_object_or_404(Post, id=id)
    if post.bookmarks.filter(id=request.user.id).exists():
        post.bookmarks.remove(request.user)
    else:
        post.bookmarks.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def archives(request, id):
    post = get_object_or_404(Post, id=id)
    if post.archive.filter(id=request.user.id).exists():
        post.archive.remove(request.user)
    else:
        post.archive.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class Penulis(View):
    template_name='users/profile.html'

    def get(self, *args, **kwargs):
        users = User.objects.get(username=self.kwargs['user'])
        posts = users.posts.filter(publish=True)
        likes = users.requirement_post_likes.all()
        archives = users.archives.all()
        views_post = users.posts.all()
        d = []
        for a in views_post:
            b = a.views
            d.append(b)

        sum_views = sum(d)

        self.context = {
            'users':users,
            'sum_views':sum_views,
            'title':'Penulis',
            'posts': posts,
            'likes': likes,
            'archives': archives,
        }
        return render(self.request, self.template_name, self.context)
