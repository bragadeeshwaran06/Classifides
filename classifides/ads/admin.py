from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'category_type')
    search_fields = ('name', 'description')
    list_filter = ('category_type',)

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'user', 'price', 'created_at')
    list_filter = ('category', 'user')
    search_fields = ('title', 'description', 'tags')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'ad', 'timestamp')
    search_fields = ('sender__username', 'receiver__username', 'ad__title', 'content')
    list_filter = ('timestamp', 'ad')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'ad')
    search_fields = ('user__username', 'ad__title')

@admin.register(AdImage)
class AdImageAdmin(admin.ModelAdmin):
    list_display = ['image']