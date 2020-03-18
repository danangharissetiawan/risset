from django.urls import path
from django.views.generic import TemplateView
from .views import register, activate, Profile, Bookmarks

app_name="users"

urlpatterns = [
    path('', Profile, name='profile'),
    path('register/', register, name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('bookmark/', Bookmarks.as_view(), name='bookmark'),
]
