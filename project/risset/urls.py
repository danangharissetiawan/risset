from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_view
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from .views import home
# from .admin import admin_site

admin.autodiscover()

urlpatterns = [
    path('', home, name='home'),
    path('home/', TemplateView.as_view(template_name='index.html'), name='home'),
    path('login/', auth_view.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(), name='logout'),
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('dashboard/', TemplateView.as_view(template_name='users/dashboard.html'), name='dashboard'),
    path('blog/', include('blog.urls', namespace='blog')),
    path('podcast/', include('podcast.urls', namespace='podcast')),
    path('users/', include('users.urls', namespace='users')),
    path('video/', include('video.urls', namespace='video')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)