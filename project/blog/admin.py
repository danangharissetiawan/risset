
import json

from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.http import JsonResponse
from django.urls import path
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


from .models import Post, Comment, Like, DisLike


# Register your models here.
admin.site.site_header = 'Risset Dashboard'

class PostAdmin(admin.ModelAdmin):
    change_list_template = 'admin/post/post_change_list.html'
    list_display = ('judul', 'user', 'likes_hit', 'dislikes_hit', 'comments_hit', 'bookmarks_hit', 'created', 'publish',)
    list_filter = ('user', 'created',)
    readonly_fields = [
        'slug',
        'bookmarks',
        'created',
        'modified',
        'publish',
        'views',
        ]
    save_as = True
    save_on_top = True
    actions = ['published']

    def changelist_view(self, request, extra_context=None):
        # Aggregate new subscribers per day
        chart_data = (
            Post.objects.annotate(date=TruncDay("created"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)

    # def get_total_likes(self, request):
    #     p = self.likes.users.count()
    #     return p


    def published(self, request, queryset):
        queryset.update(publish=True)

admin.site.register(Post, PostAdmin)
admin.site.unregister(Group)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'body', 'created', 'activate',)
    list_filter = ('post', 'created',)
    readonly_fields = [
        'created',
        'activate',
    ]
    actions = ['active']

    def active(self, request, queryset):
        queryset.update(activate=True)


admin.site.register(Comment, CommentAdmin)
    

# class LikeAdmin(admin.ModelAdmin):
#     list_display = ('post', 'users', 'created_at',)
    


admin.site.register(Like)
admin.site.register(DisLike)

    

