
from django.contrib import admin
from .models import User, Product, Order, OrderItem, Comment, Post

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Comment)
admin.site.register(Post)



