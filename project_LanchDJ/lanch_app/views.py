from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem, Comment, Post
from django.contrib.auth import login, authenticate
from .forms import SignUpForm

# Главная страница
def index(request):
    return render(request, 'index.html')

# Страница меню
def menu(request):
    products = Product.objects.all()
    return render(request, 'menu.html', {'products': products})

# Страница заказа
@login_required
def order(request):
    order_items = OrderItem.objects.filter(order__user=request.user)
    total_price = sum(item.product.price * item.quantity for item in order_items)
    return render(request, 'order.html', {'order_items': order_items, 'total_price': total_price})

# Страница информации
def info(request):
    comments = Comment.objects.all()
    posts = Post.objects.all()
    return render(request, 'info.html', {'comments': comments, 'posts': posts})

# Добавление товара в корзину
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order, created = Order.objects.get_or_create(user=request.user, defaults={'total_price': 0})
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    order_item.quantity += 1
    order_item.save()
    order.total_price += product.price
    order.save()
    return redirect('menu')

# Удаление товара из корзины
@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order = get_object_or_404(Order, user=request.user)
    order_item = get_object_or_404(OrderItem, order=order, product=product)
    order_item.quantity -= 1
    if order_item.quantity <= 0:
        order_item.delete()
    else:
        order_item.save()
    order.total_price -= product.price
    if order.total_price < 0:
        order.total_price = 0
    order.save()
    return redirect('order')



