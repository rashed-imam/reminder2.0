from django.contrib import admin
from django.db.models import Q

from .models import Item, TagCategory
from .models import Tag, Section, Document, URLResource
from django.utils.translation import gettext_lazy as _


# Register your models here.

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(TagCategory)
class TagCategoryAdmin(admin.ModelAdmin):
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

class TagFilter(admin.SimpleListFilter):
    title = _('Tags')  # Display name for the filter
    parameter_name = 'tags'  # URL parameter name for filtering

    def lookups(self, request, model_admin):
        tags = Tag.objects.all()
        return [(tag.id, tag.name) for tag in tags]

    def queryset(self, request, queryset):
        if self.value():
            tag_ids = self.value().split(',')
            q_objects = Q()
            for tag_id in tag_ids:
                q_objects |= Q(tags__id=tag_id)
            return queryset.filter(q_objects)
        return queryset

# Define a custom filter for TagCategory
class TagCategoryFilter(admin.SimpleListFilter):
    title = _('Tag Category')  # Display name for the filter
    parameter_name = 'tag_category'  # URL parameter name for filtering

    def lookups(self, request, model_admin):
        # Retrieve all distinct tag categories associated with items
        categories = TagCategory.objects.filter(tag__isnull=False).distinct()
        return [(category.id, category.name) for category in categories]

    def queryset(self, request, queryset):
        # Apply filter if a category is selected
        if self.value():
            return queryset.filter(tags__category_id=self.value())


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'get_tags', 'url_resource', 'is_published')
    list_filter = ('section', 'url_resource', 'is_published', TagCategoryFilter)
    search_fields = ('title', 'description', 'tags__name', 'section__name')

    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])

    get_tags.short_description = 'Tags'
