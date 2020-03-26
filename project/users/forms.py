from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, UserFollowing
from blog.models import Post
from ckeditor_uploader.fields import RichTextUploadingField


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    
class ProfileUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['foto', 'alamat', 'status']


# class UserFollowingForm(forms.ModelForm):
    
#     class Meta:
#         model = UserFollowing
#         fields = ("user_id", "following_user_id", "created",)


class PostForm(forms.ModelForm):
    # judul = forms.CharField(required=False)
    # thumbnail = forms.ImageField(required=False)
    # atrikel = forms.CharField(widget=RichTextUploadingField(config_name="special"))
    class Meta:
        model = Post
        fields = ('judul','thumbnail', 'atrikel',)
        widgets = {
            'atrikel':  forms.CharField(widget=RichTextUploadingField(config_name="special"))
        }