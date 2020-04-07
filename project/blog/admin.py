
import json


from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.http import JsonResponse
from django.urls import path
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


from .models import Post, Comment, Like, DisLike, Kategori


# Register your models here.
admin.site.site_header = 'Risset Dashboard'
# admin.site.index_template = 'admin/index_chart.html'


class PostAdmin(admin.ModelAdmin):
    change_list_template = 'admin/post/post_change_list.html'
    list_display = ('judul', 'user', 'likes_hit', 'dislikes_hit', 'comments_hit', 'bookmarks_hit', 'created', 'publish',)
    list_display_links = ('judul',)
    list_filter = ('user', 'created',)
    search_fields = ('judul', 'kategori', 'tags')
    readonly_fields = ['slug', 'bookmarks', 'created', 'modified', 'publish', 'views',]
    fieldsets = (
        (None, {
            'fields':('user','judul','tags','kategori', 'atrikel', 'thumbnail',)
        }),
        ('Advanced options', {
            'classes':('collapse',),
            'fields':('slug','created','modified','publish'),
        }),
        
    )
    save_as = True
    save_on_top = True
    actions = ['published']

    def get_search_results(self, request, queryset, search_term):
        queryset, user_distinct = super().get_search_results(request, queryset, search_term)
        try:
            search_term_as_int = int(search_term)
        except ValueError:
            pass
        else:
            queryset |= self.model.objects.filter(judul=search_term_as_int)
        return queryset, user_distinct

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


    def published(self, request, queryset):
        queryset.update(publish=True)

admin.site.register(Post, PostAdmin)
# admin.site.unregister(Group)
admin.site.register(Kategori)

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

    

