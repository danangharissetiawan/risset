from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Post, Comment, Like, DisLike, Kategori
from .forms import CommentForm



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

        user = self.request.user
        self.kwargs.update({'users':user})


        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        context["title"] = "Blog - "
        context["active"] = "active"
        return context


class PostDetailView(View):
    model = Post
    template_name = "blog/detail.html"
    comment_form = CommentForm()
    is_bookmarks = False


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
            'title':'Post',
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
            return redirect('blog:detail', post.slug)
        return redirect('blog:detail', post.slug)


def bookmarks(request, id):
    post = get_object_or_404(Post, id=id)
    if post.bookmarks.filter(id=request.user.id).exists():
        post.bookmarks.remove(request.user)
    else:
        post.bookmarks.add(request.user)
    return HttpResponseRedirect(post.get_absolute_url())


class Penulis(View):
    template_name='users/profile.html'

    def get(self, *args, **kwargs):
        users = User.objects.get(username=self.kwargs['user'])
        views_post = users.posts.all()
        d = []
        for a in views_post:
            b = a.views
            d.append(b)

        sum_views = sum(d)

        self.context = {
            'users':users,
            'sum_views':sum_views
        }
        return render(self.request, self.template_name, self.context)