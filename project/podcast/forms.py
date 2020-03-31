from django import forms

from .models import PodcastComment


class PodcastCommentForm(forms.ModelForm):
    
    class Meta:
        model = PodcastComment
        fields = ("body",)
