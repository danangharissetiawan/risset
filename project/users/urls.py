from django.urls import path
from django.views.generic import TemplateView
from .views import register, activate, Profile, Bookmarks,  Follow, tambah_artikel

app_name="users"

urlpatterns = [
    path('', Profile, name='profile'),
    path('follow/<user_id>', Follow.as_view(), name='follow'),
    path('tambah-artikel/', tambah_artikel, name="tambah-artikel"),
    path('register/', register, name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('bookmark/', Bookmarks.as_view(), name='bookmark'),
]
