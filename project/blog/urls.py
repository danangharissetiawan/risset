from django.urls import path
from django.views.generic import TemplateView

from .views import PostListView, PostDetailView, LikeDislike, Comment, bookmarks, Penulis, archives, AllPost, Tags, search

app_name = "blog"

urlpatterns = [
    path('', AllPost.as_view(), name='home'),
    path('videos/', TemplateView.as_view(template_name='blog/videos.html'), name='videos'),
    path('post/<slug>/', PostDetailView.as_view(), name='detail'),
    path('tags/<str:tag>', Tags.as_view(), name='tag'),
    path('search/',search, name='search' ),
    path('requirement/<int:post_id>/<str:opinion>', LikeDislike.as_view(), name='like_dislike'),
    path('comment/<str:slug>', Comment.as_view(), name='comment'),
    path('video-detail/', TemplateView.as_view(template_name='blog/single-video.html'), name='video-detail'),
    path('bookmarks/<int:id>', bookmarks, name='bookmarks'),
    path('archives/<int:id>', archives, name='archives'),
    path('penulis/<str:user>', Penulis.as_view(), name='penulis'),
    path('profile/', TemplateView.as_view(template_name='blog/profile.html'), name='profile'),
    path('<kategori>/', PostListView.as_view(), name='kategori'),
]
