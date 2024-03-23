from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVectorField
from django.db import models


class BaseModel(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('disabled', 'Disabled'),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_created_by', null=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_updated_by', null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='draft')
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_reviewer', null=True)

    class Meta:
        abstract = True


class TagCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(TagCategory, on_delete=models.SET_NULL, related_name='%(class)s',null=True)

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Document(models.Model):
    DOC_TYPES = (
        ('PDF', 'Pdf'),
        ('DOC', 'Document'),
        ('TXT', 'Text'),
        ('IMAGE', 'Image'),
        ('AUDIO', 'Audio'),
        ('VIDEO', 'Video'),
    )

    name = models.CharField(max_length=50)
    file = models.FileField(upload_to='documents/', blank=True, null=True)
    doctype = models.CharField(max_length=10, choices=DOC_TYPES)

    def __str__(self):
        return self.name + self.doctype


class URLResource(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Item(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="tagged_items")
    section = models.ForeignKey(Section, related_name="items_in_section", on_delete=models.CASCADE)
    url_resource = models.ForeignKey(URLResource, related_name="linked_items", on_delete=models.CASCADE)
    documents = models.ForeignKey(Document, blank=True, null=True, on_delete=models.SET_NULL)
    is_published = models.BooleanField(default=False)
    # meta = JSONField(default=dict)

    search_vector = SearchVectorField(null=True)

    def __str__(self):
        return self.title


# @receiver(post_save, sender=Item)
# def update_search_vector(sender, instance, **kwargs):
#     instance.search_vector = SearchVector('title', 'description')
#
#     # Update search vector based on tags and section
#     tags_search_vector = SearchVector('tags__name', config='english')
#     section_search_vector = SearchVector('section__name', config='english')
#     instance.search_vector = instance.search_vector.bitor(tags_search_vector).bitor(section_search_vector)
#     instance.save()


    # You may need to add additional logic for handling tag and section updates
