from django.urls import path
from django.views.generic import TemplateView

from .views import AllPodcast, PodcastListView, TagsPodcast, PodcastDetailView, PodcastComment, PodcastLikeDislike, PenulisPodcast, podcast_bookmarks, podcast_archives

app_name = "podcast"

urlpatterns = [
    path('', AllPodcast.as_view(), name='home'),
    path('<str:kategori>/', PodcastListView.as_view(), name='kategori'),
    path('post/<str:slug>/', PodcastDetailView.as_view(), name='detail'),
    path('comment/<str:slug>', PodcastComment.as_view(), name='comment'),
    path('requirement/<int:podcast_id>/<str:opinion>', PodcastLikeDislike.as_view(), name='like_dislike'),
    path('tag/<str:tag>/', TagsPodcast.as_view(), name='tag'),
    path('detail/', TemplateView.as_view(template_name='podcast/single-podcast.html'), name='detail'),
    path('bookmarks/<int:id>', podcast_bookmarks, name='bookmarks'),
    path('archives/<int:id>', podcast_archives, name='archives'),
    path('penulis/<str:user>/', PenulisPodcast.as_view(), name='penulis'),
]
