from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Kategori(models.Model):
    kategori = models.CharField(max_length=125)

    def __str__(self):
        return self.kategori


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    judul = models.CharField(max_length=125)
    thumbnail = models.ImageField(upload_to='blog/post')
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE, blank=True, null=True, related_name='kategoris')
    tags = TaggableManager(blank=True)
    atrikel = RichTextUploadingField(blank=True, null=True, config_name='default')
    views = models.PositiveIntegerField(default=0)
    bookmarks = models.ManyToManyField(User, related_name='bookmarks', blank=True)
    archive = models.ManyToManyField(User, related_name="archives", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    publish = models.BooleanField(default=False, editable=False)
    slug = models.SlugField(blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.judul)
        super(Post, self).save(*args, **kwargs)
    
    def likes_hit(self):
        return self.likes.users.count()

    def dislikes_hit(self):
        return self.dis_likes.users.count()

    def bookmarks_hit(self):
        return self.bookmarks.count()

    def comments_hit(self):
        return self.comments.count()

    def __str__(self):
        return self.judul

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    reply = models.ForeignKey("Comment", related_name='replies', on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    activate = models.BooleanField(default=False)
    

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return "{} by {}".format(self.user.username, self.post)

    # def get_absolute_url(self):
    #     return reverse("Comment_detail", kwargs={"pk": self.pk})


class Like(models.Model):
    post = models.OneToOneField(Post, related_name="likes", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='requirement_post_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.post.judul)


class DisLike(models.Model):
    post = models.OneToOneField(Post, related_name="dis_likes", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='requirement_post_dis_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.post.judul)
