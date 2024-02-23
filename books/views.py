from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import ListView, DetailView

from .models import Books
from .utils import DataMixin


class BooksHome(DataMixin, ListView):
    model = Books
    template_name = 'books/index.html'
    context_object_name = 'items'
    title_page = 'Главная страница'


class Catalog(DataMixin, ListView):
    model = Books
    template_name = 'books/catalog.html'
    context_object_name = 'items'
    title_page = 'Каталог'

    def get_ordering(self):
        ordering = self.request.GET.get('order_by', None)
        return ordering


class Search(DataMixin, ListView):
    model = Books
    context_object_name = 'items'
    template_name = 'books/catalog.html'
    title_page = 'Поиск'

    def get_queryset(self):
        ordering = self.request.GET.get('order_by', None)
        result = Books.objects.filter(Q(title__icontains=self.request.GET.get('q')) |
                                      Q(author__last_name__icontains=self.request.GET.get('q')))
        if ordering:
            return result.order_by(ordering)
        return result


class ShowItem(DataMixin, DetailView):
    model = Books
    template_name = 'books/item.html'
    slug_url_kwarg = 'item_slug'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['item'].title)


class BooksFilterByAuthor(DataMixin, ListView):
    template_name = 'books/catalog.html'
    context_object_name = 'items'

    def get_queryset(self):
        ordering = self.request.GET.get('order_by', None)
        result = Books.objects.filter(author__slug=self.kwargs['author_slug']).select_related('author')

        if ordering:
            return result.order_by(ordering)
        return result

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        author = context['items'][0].author
        return self.get_mixin_context(context, title='Автор - ' + author.last_name)
