from random import random

from django.shortcuts import render

from .forms import SearchForm
from .models import Item, Tag


def search_items(tags):
    # Assuming tags is a list of tag names
    items = Item.objects.filter(tags__name__in=tags).distinct()
    return items


def search_view(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        print('Searching')
        if form.is_valid():
            tags = form.cleaned_data['tags'].split(',')
            print(tags)
            items = search_items(tags)
            print('Searching' + items)
            return render(request, 'search_results.html', {'items': items})
    else:
        form = SearchForm()
    return render(request, 'search_form.html', {'form': form})


def populate_items(request):
    # Define the relevant tags
    relevant_tags = [
        "ramadan", "friday", "Thursday", "monday", "parent", "business",
        "employer", "employee", "brother", "sister", "father", "mother",
        "husband", "wife", "son", "married", "female", "male", "evening",
        "morning"
    ]

    # Number of items to populate
    num_items = 10

    # Populate items
    for _ in range(num_items):
        # Randomly select tags for each item
        num_tags = random.randint(1, 5)  # Random number of tags per item
        selected_tags = random.sample(relevant_tags, num_tags)

        # Create item instance
        item = Item.objects.create(
            title=f"Title {random.randint(1, 100)}",
            description=f"Description {random.randint(1, 100)}",
        )

        # Assign selected tags to the item
        for tag_name in selected_tags:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            item.tags.add(tag)
