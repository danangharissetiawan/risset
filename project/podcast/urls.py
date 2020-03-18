from django.urls import path
from django.views.generic import TemplateView

app_name = "podcast"

urlpatterns = [
    path('', TemplateView.as_view(template_name='podcast/podcast.html'), name='home'),
    path('detail/', TemplateView.as_view(template_name='podcast/single-podcast.html'), name='detail'),
]
