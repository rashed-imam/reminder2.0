from django.contrib import admin
from .models import Tag, Section, Document, URLResource, Item


# Register your models here.

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'doctype')


@admin.register(URLResource)
class URLResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'url_resource', 'is_published')  # Removed 'created_at' and 'updated_at'
    list_filter = ('section', 'url_resource', 'is_published')
    search_fields = ('title', 'description', 'tags__name', 'section__name')
