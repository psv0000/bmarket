from django.db import models

from books.models import Books
from users.models import User


class CartQueryset(models.QuerySet):

    def total_price(self):
        return sum(cart.item_price() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Cart(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')
    item = models.ForeignKey(to=Books, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')
    session_key = models.CharField(max_length=32, null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        db_table = 'carts'
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    objects = CartQueryset().as_manager()

    def __str__(self):
        if self.user:
            return f'Корзина {self.user.username} | Товар {self.item.title} | Количество {self.quantity}'

        return f'Анонимная корзина | Товар {self.item.title} | Количество {self.quantity}'

    def item_price(self):
        return self.item.price * self.quantity
