from django import template
from django.utils.http import urlencode

from books.models import Authors

register = template.Library()


@register.inclusion_tag('books/list_of_authors.html')
def show_authors():
    authors = Authors.objects.all()
    return {'authors': authors}


@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)
