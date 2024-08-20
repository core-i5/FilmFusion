from django.contrib import admin
from .models import Review, Comment

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie', 'user', 'content', 'rating', 'created_at', 'updated_at')
    search_fields = ('user__name', 'movie__title', 'content')
    list_filter = ('created_at', 'updated_at', 'user')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'review', 'user', 'content', 'created_at', 'updated_at')
    search_fields = ('user__name', 'review__movie__title', 'content')
    list_filter = ('created_at', 'updated_at', 'user')


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)