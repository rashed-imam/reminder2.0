# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_view, name='search'),
    path('populate/', views.populate_items, name='populate'),
]
