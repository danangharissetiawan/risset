from django.contrib import admin
from django.contrib.auth.models import User

from .models import Podcast, PodcastLike, PodcastDisLike, PodcastComment, PodcastKategori

# Register your models here.

class PodcastAdmin(admin.ModelAdmin):
    list_display = ('judul', 'user', 'podcast_likes_hint', 'podcast_dislikes_hint', 'podcast_comments_hint', 'bookmark_hint', 'created', 'publish')
    list_filter = ('user', 'created',)
    readonly_fields = [
        'slug',
        'bookmark',
        'created',
        'modified',
        'publish',
        'views',
        ]
    actions = ['published']


    def published(self, request, queryset):
        queryset.update(publish=True)

admin.site.register(Podcast, PodcastAdmin)
# admin.site.unregister(Group)
admin.site.register(PodcastKategori)

class PodcastCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'podcast', 'body', 'created', 'activate',)
    list_filter = ('podcast', 'created',)
    readonly_fields = [
        'created',
        'activate',
    ]
    actions = ['active']

    def active(self, request, queryset):
        queryset.update(activate=True)


admin.site.register(PodcastComment, PodcastCommentAdmin)
    

# class LikeAdmin(admin.ModelAdmin):
#     list_display = ('post', 'users', 'created_at',)
    


admin.site.register(PodcastLike)
admin.site.register(PodcastDisLike)