from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Product, Order, OrderItem, Comment, Post
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
    # Получаем все товары в заказе текущего пользователя
    order_items = OrderItem.objects.filter(order__user=request.user)

    # Для каждого товара в заказе вычисляем его общую стоимость и добавляем в объект
    for item in order_items:
        item.total_price = item.product.price * item.quantity

    # Вычисляем общую сумму заказа
    total_price = sum(item.total_price for item in order_items)

    # Передаем данные в шаблон
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

    # При создании нового OrderItem сразу инициализируем поле quantity значением 1
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product, defaults={'quantity': 1})

    if not created:
        # Если элемент заказа уже существовал, увеличиваем его количество
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

# Авторизация пользователя
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))  # Перенаправление на главную страницу
        else:
            return render(request, 'login.html', {'error_message': 'Неправильное имя пользователя или пароль.'})
    return render(request, 'login.html')

# Функция регистрации нового пользователя
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# Выход пользователя из системы
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

