from django.urls import path

from carts import views

app_name = 'carts'

urlpatterns = [
    path('details', views.get_user_cart, name='details'),
    path('cart_add/<slug:item_slug>', views.cart_add, name='cart_add'),
    path('add_cart_item/<int:cart_id>', views.add_cart_item, name='add_cart_item'),
    path('reduce_cart_item/<int:cart_id>', views.reduce_cart_item, name='reduce_cart_item'),
    path('cart_remove/<int:cart_id>', views.cart_remove, name='cart_remove'),
    path('create_order/', views.create_order, name='create_order'),
]
