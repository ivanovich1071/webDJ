
from django.contrib import admin
from .models import User, Product, Order, OrderItem, Comment, Post

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Comment)
admin.site.register(Post)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image_preview', 'description')
    search_fields = ('name', 'description')
    list_filter = ('price',)
    ordering = ('name',)

    # Добавляем метод для отображения превью изображения
    def image_preview(self, obj):
        return obj.image_url and obj.image_url.url

    image_preview.short_description = 'Превью изображения'
    image_preview.allow_tags = True

