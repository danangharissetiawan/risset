from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings
from taggit.managers import TaggableManager

# Create your models here.

class PodcastKategori(models.Model):
    kategori = models.CharField(max_length=50)


    def __str__(self):
        return self.kategori


class Podcast(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='podcasts')
    judul = models.CharField(max_length=125)
    kategori = models.ForeignKey(PodcastKategori, on_delete=models.CASCADE, related_name='podcast_kategoris', blank=True, null=True)
    tags = TaggableManager(blank=True)
    podcast = models.FileField(upload_to='podcast/post')
    deskripsi = models.TextField()
    views = models.PositiveIntegerField(default=0)
    bookmark = models.ManyToManyField(User, related_name='podcast_bookmarks', blank=True)
    archive = models.ManyToManyField(User, related_name="podcast_archives", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    publish = models.BooleanField(default=False, editable=False)
    slug = models.SlugField(blank=True, null=True, editable=False)
    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.judul)
        super(Podcast, self).save(*args, **kwargs)
    
    def podcast_likes_hint(self):
        return self.podcast_likes.users.count()

    def podcast_dislikes_hint(self):
        return self.podcast_dis_likes.users.count()

    def bookmark_hint(self):
        return self.bookmark.count()

    def podcast_comments_hint(self):
        return self.podcast_comments.count()

    def __str__(self):
        return self.judul

    def get_absolute_url(self):
        return reverse("podcast:detail", kwargs={"slug": self.slug})


class PodcastComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='podcast_users')
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE, related_name='podcast_comments')
    body = models.TextField()
    reply = models.ForeignKey('PodcastComment', related_name='podcast_replies', on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    activate = models.BooleanField(default=False)
    

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return "{} by {}".format(self.user.username, self.podcast)


class PodcastLike(models.Model):
    podcast = models.OneToOneField(Podcast, related_name="podcast_likes", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='requirement_podcast_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.podcast.judul)


class PodcastDisLike(models.Model):
    podcast = models.OneToOneField(Podcast, related_name="podcast_dis_likes", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='requirement_podcast_dis_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.podcast.judul)
