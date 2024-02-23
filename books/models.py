from django.db import models
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from slugify import slugify


class Books(models.Model):
    title = models.CharField(max_length=100, verbose_name='Наименование')
    slug = AutoSlugField(populate_from='title', slugify_function=slugify, max_length=100, verbose_name='Slug')
    description = models.TextField(blank=True, verbose_name='Описание')
    image = models.ImageField(blank=True, null=True, default=None, verbose_name='Изображение')
    amount = models.IntegerField(default=10, verbose_name='Количество')
    price = models.IntegerField(default=0, verbose_name='Цена')
    author = models.ForeignKey('Authors', on_delete=models.PROTECT, related_name='book', null=True)

    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Книги'
        verbose_name_plural = 'Книги'
        indexes = [
            models.Index(fields=['slug'])
        ]

    def get_absolute_url(self):
        return reverse('item', kwargs={'item_slug': self.slug})


class Authors(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    middle_name = models.CharField(max_length=100, verbose_name='Отчество/Второе имя')
    last_name = models.CharField(max_length=100, blank=True, verbose_name='Фамилия')
    slug = AutoSlugField(populate_from='last_name', slugify_function=slugify, max_length=100)

    def __str__(self):
        return self.last_name

    def get_absolute_url(self):
        return reverse('author', kwargs={'author_slug': self.slug})
