# from your_app.models import Item, Tag, Section, URLResource, Document
import random
import string

from django.core.management.base import BaseCommand

from search.models import Section, Item, URLResource, Tag, Document


from django.core.management.base import BaseCommand


# class Command(BaseCommand):
#     help = 'My custom command description'
#
#     def handle(self, *args, **options):
#         # Your command logic goes here
#         self.stdout.write(self.style.SUCCESS('Successfully ran my custom command'))


def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters, k=length))


def create_random_item():
    title = generate_random_string(10)
    description = generate_random_string(50)
    section = Section.objects.order_by('?').first()  # Randomly select a section
    url_resource = URLResource.objects.order_by('?').first()  # Randomly select a URLResource
    is_published = random.choice([True, False])

    item = Item.objects.create(
        title=title,
        description=description,
        section=section,
        url_resource=url_resource,
        is_published=is_published
    )

    # Add random tags to the item
    tags_count = random.randint(1, 3)  # Randomly select 1 to 3 tags
    tags = Tag.objects.order_by('?')[:tags_count]
    item.tags.add(*tags)

    # Add a random document to the item
    document = Document.objects.order_by('?').first()  # Randomly select a document
    item.documents = document
    item.save()


class Command(BaseCommand):
    help = 'Populate the database with 1000 Item instances'

    def handle(self, *args, **kwargs):
        self.stdout.write("Populating the database with 1000 Item instances...")
        for _ in range(1000):
            create_random_item()
        self.stdout.write(self.style.SUCCESS("Database populated successfully."))
