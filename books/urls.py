from django.urls import path
from . import views

urlpatterns = [
    path('', views.BooksHome.as_view(), name='home'),
    path('catalog/', views.Catalog.as_view(), name='catalog'),
    path('item/<slug:item_slug>/', views.ShowItem.as_view(), name='item'),
    path('catalog/author/<slug:author_slug>/', views.BooksFilterByAuthor.as_view(), name='author'),
    path('catalog/search/', views.Search.as_view(), name='search'),
]
