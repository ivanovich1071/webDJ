from django.db import models
from django.contrib.auth.models import AbstractUser

# Модель пользователя

class User(AbstractUser):
    telephon = models.CharField(max_length=15, unique=True, verbose_name="Телефон")
    is_admin = models.BooleanField(default=False, verbose_name="Администратор")

    def __str__(self):
        return self.username
# Модель продукта
class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image_url = models.ImageField(upload_to='images/', verbose_name="Изображение")

    def __str__(self):
        return self.name

# Модель заказа
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="Пользователь")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая цена")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'

# Модель элемента заказа
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items', verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', verbose_name="Продукт")
    quantity = models.PositiveIntegerField(verbose_name="Количество")

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

# Модель комментария
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name="Пользователь")
    content = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f'Comment by {self.user.username}'

# Модель поста
class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    video_url = models.FileField(upload_to='video/', verbose_name="Видео")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title
from django.db import models


