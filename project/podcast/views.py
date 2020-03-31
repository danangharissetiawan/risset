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

from .models import Podcast, PodcastComment, PodcastDisLike, PodcastKategori, PodcastLike
from .forms import PodcastCommentForm

# Create your views here.

class AllPodcast(ListView):
    model = Podcast
    template_name = 'podcast/podcast.html'
    context_object_name = 'podcasts'
    ordering = '-created'
    # paginate_by = 10

    def get_context_data(self, **kwargs):
        kategori_list = PodcastKategori.objects.all()
        self.kwargs.update({'kategori_list':kategori_list})

        user = self.request.user
        self.kwargs.update({'users':user})


        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        context["title"] = "Podcast"
        context["active"] = "active"
        return context


class PodcastListView(ListView):
    model = Podcast
    template_name = "podcast/podcast.html"
    context_object_name = 'podcasts'
    ordering = "-created"
    # paginate_by = 10

    def get_queryset(self):
        b = PodcastKategori.objects.get(kategori=self.kwargs['kategori'])
        self.queryset = b.podcast_kategoris.all()
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        kategori_list = PodcastKategori.objects.all().exclude(kategori=self.kwargs['kategori'])
        self.kwargs.update({'kategori_list':kategori_list})

        kategori_active = PodcastKategori.objects.get(kategori=self.kwargs['kategori'])
        self.kwargs.update({'kategori_active':kategori_active})
        print(kategori_active)

        user = self.request.user
        self.kwargs.update({'users':user})


        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        context["title"] = kategori_active
        context["active"] = "active"
        return context


class TagsPodcast(ListView):
    # model = Post
    template_name = "podcast/podcast.html"
    context_object_name = 'podcasts'
    ordering = '-created'
    # paginate_by = 10

    def get_queryset(self):
        self.queryset = Podcast.objects.filter(tags__name__contains=self.kwargs['tag'])
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        kategori_list = PodcastKategori.objects.all()
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


class PodcastDetailView(View):
    model = Podcast
    template_name = "podcast/single-podcast.html"
    comment_form = PodcastCommentForm()
    is_bookmarks = False
    is_archives = False


    def get(self, *args, **kwargs):
        podcast = self.model.objects.get(slug=self.kwargs['slug'])
        podcast.views = podcast.views+1
        podcast.save()

        if podcast.bookmark.filter(id=self.request.user.id):
            self.is_bookmarks = True;


        comments = podcast.podcast_comments.filter(activate=True, reply=None).order_by('-created')
        j_comments = podcast.podcast_comments.filter().order_by('-created')

        self.context = {
            'podcast':podcast,
            'comment_form':self.comment_form,
            'is_bookmarks': self.is_bookmarks,
            'comments':comments,
            'jumlah_comment': j_comments,
            'title':podcast,
        }
        return render(self.request, self.template_name, self.context)


class PodcastComment(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'
    model = PodcastComment

    def post(self, *args, **kwargs):
        podcast = Podcast.objects.get(slug=kwargs['slug'])
        podcast_comments = self.model.objects.filter(activate=True, reply=None).order_by('-created')
        if self.request.method == 'POST':
            self.comment_form = PodcastCommentForm(self.request.POST or None)
            if self.comment_form.is_valid():
                new_comment = self.comment_form.save(commit=False)
                reply_id = self.request.POST.get('reply')
                comment_qs = None
                if reply_id:
                    comment_qs = podcast.podcast_comments.get(id=reply_id)
                new_comment.reply = comment_qs
                new_comment.user = self.request.user
                new_comment.podcast = podcast
                new_comment.save()
                messages.success(self.request, "Komentar terkirin! sedang menunggu moderasi")
        return redirect('podcast:detail', kwargs['slug'])


class PodcastLikeDislike(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        # p = Post.objects.get(slug=kwargs['slug'])
        # print(p)
        podcast_id = self.kwargs.get('podcast_id', None)
        opinion = self.kwargs.get('opinion', None) #like atau dislike

        podcast = get_object_or_404(Podcast, id=podcast_id)

        try:
            podcast.podcast_dis_likes
        except Podcast.podcast_dis_likes.RelatedObjectDoesNotExist as identifier:
            PodcastDisLike.objects.create(podcast=podcast)

        try:
            podcast.podcast_likes
        except Podcast.podcast_likes.RelatedObjectDoesNotExist as identifier:
            PodcastLike.objects.create(podcast=podcast)

        if opinion.lower() == 'like':
            if request.user in podcast.podcast_likes.users.all():
                podcast.podcast_likes.users.remove(request.user)
            else:
                podcast.podcast_likes.users.add(request.user)
                podcast.podcast_dis_likes.users.remove(request.user)
        elif opinion.lower() == 'dis_like':
            if request.user in podcast.podcast_dis_likes.users.all():
                podcast.podcast_dis_likes.users.remove(request.user)
            else:
                podcast.podcast_dis_likes.users.add(request.user)
                podcast.podcast_likes.users.remove(request.user)
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def podcast_bookmarks(request, id):
    podcast = get_object_or_404(Podcast, id=id)
    if podcast.bookmark.filter(id=request.user.id).exists():
        podcast.bookmark.remove(request.user)
    else:
        podcast.bookmark.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def podcast_archives(request, id):
    podcast = get_object_or_404(Podcast, id=id)
    if podcast.archive.filter(id=request.user.id).exists():
        podcast.archive.remove(request.user)
    else:
        podcast.archive.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



class PenulisPodcast(View):
    template_name='users/profile.html'

    def get(self, *args, **kwargs):
        users = User.objects.get(username=self.kwargs['user'])
        podcasts = users.podcasts.filter(publish=True)
        # likes = users.requirement_post_likes.all()
        # archives = users.archives.all()
        views_podcasts = users.podcasts.all()
        d = []
        for a in views_podcasts:
            b = a.views
            d.append(b)

        sum_views = sum(d)

        self.context = {
            'users':users,
            'sum_views':sum_views,
            'title':'Penulis Podcast',
            'podcasts': podcasts,
            # 'likes': likes,
            # 'archives': archives,
        }
        return render(self.request, self.template_name, self.context)
