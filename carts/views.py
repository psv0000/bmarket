from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.forms import ValidationError

from books.models import Books
from carts.models import Cart
from users.models import User


def get_user_cart(request):
    return render(request, 'cart/details.html')


def cart_add(request, item_slug):
    item = Books.objects.get(slug=item_slug)

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, item=item)

        if carts.exists():
            carts = carts.first()
            carts.quantity += 1
            carts.save()
        else:
            Cart.objects.create(user=request.user, item=item, quantity=1)

    else:
        carts = Cart.objects.filter(session_key=request.session.session_key, item=item)

        if carts.exists():
            cart = carts.first()
            cart.quantity += 1
            cart.save()
        else:
            Cart.objects.create(session_key=request.session.session_key, item=item, quantity=1)

    return redirect(request.META.get('HTTP_REFERER'))


def add_cart_item(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    cart.quantity += 1
    cart.save()

    return redirect(request.META.get('HTTP_REFERER'))


def reduce_cart_item(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    cart.quantity -= 1
    cart.save()

    return redirect(request.META.get('HTTP_REFERER'))


def cart_remove(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    cart.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def create_order(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                user = request.user
                cart_items = Cart.objects.filter(user=user)

                if cart_items.exists():

                    total_cart_price = 0
                    for cart_item in cart_items:
                        if cart_item.item.amount < cart_item.quantity:
                            raise ValidationError(f'Недостаточное количество товара "{cart_item.item.title}",\
                                                   в наличии - {cart_item.item.amount}.')

                        if user.purse < cart_item.item.price:
                            raise ValidationError(f'Недостаточное монет в кошельке для оплаты товара '
                                                  f'"{cart_item.item.title}", баланс - {user.purse} У.Е.')

                        book_remains = cart_item.item.amount - cart_item.quantity
                        Books.objects.filter(title=cart_item.item.title).update(amount=book_remains)

                        total_cart_price += cart_item.item_price()

                    if user.purse < total_cart_price:
                        raise ValidationError(f'Недостаточное монет в кошельке для оплаты товаров на сумму '
                                              f'{total_cart_price} У.Е., баланс - {user.purse} У.Е.')

                    purse_remains = user.purse - total_cart_price
                    User.objects.filter(username=user.username).update(purse=purse_remains)

                    cart_items.delete()

                    return render(request, 'cart/order_done.html')

        except ValidationError as error:
            messages.info(request, list(error)[0])
            return render(request, 'cart/validation_error.html')

    return redirect('home')
