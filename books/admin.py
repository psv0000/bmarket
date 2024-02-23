from django.contrib import admin

from .models import Books


@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'description', 'image', 'amount', 'price', 'author']
    readonly_fields = ['slug']
    list_display = ['id', 'title', 'slug', 'amount', 'price']
    list_display_links = ['id', 'title']
