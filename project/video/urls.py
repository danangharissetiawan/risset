from django.urls import path
from django.views.generic import TemplateView

app_name="video"

urlpatterns = [
    path('', TemplateView.as_view(template_name='video/videos.html'), name='home'),
    path('detail/', TemplateView.as_view(template_name='video/single-video.html'), name='detail'),
]
