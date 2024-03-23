from django.contrib import admin

from .models import Item
from .models import Tag, Section, Document, URLResource


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


class TagsFilter(admin.RelatedFieldListFilter):
    def field_choices(self, field, request, model_admin):
        # Get the queryset for the related model of the ManyToManyField
        related_model = field.remote_field.model
        queryset = related_model.objects.all()
        return [(tag.pk, str(tag)) for tag in queryset]

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'get_tags', 'url_resource', 'is_published')
    list_filter = ('section', 'url_resource', 'is_published', ('tags', TagsFilter))
    search_fields = ('title', 'description', 'tags__name', 'section__name')

    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])

    get_tags.short_description = 'Tags'
