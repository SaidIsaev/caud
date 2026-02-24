# products/models.py
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    class Meta:
        db_table = 'category'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    def __str__(self): return self.name

class Manufacturer(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    class Meta:
        db_table = 'manufacturer'
        verbose_name = 'Производитель'
    def __str__(self): return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    class Meta:
        db_table = 'supplier'
        verbose_name = 'Поставщик'
    def __str__(self): return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products', verbose_name='Категория')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT, related_name='products', verbose_name='Производитель')
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='products', verbose_name='Поставщик')
    
    SKU = models.CharField(max_length=20, unique=True, verbose_name='Артикул', default=0)
    name = models.CharField(max_length=200, verbose_name='Наименование')
    description = models.TextField(blank=True, verbose_name='Описание')
    unit_type = models.CharField(max_length=20, default='шт.', verbose_name='Единица измерения')
    
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Скидка %')
    
    stock_quantity = models.IntegerField(default=0, verbose_name='Количество на складе')
    
    image = models.CharField(max_length=100, blank=True, null=True, verbose_name='Фото (имя файла)')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        db_table = 'product'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.name} {self.manufacturer} {self.SKU}'
    
    @property
    def final_price(self):
        """Цена со скидкой — для шаблона"""
        if self.discount > 0:
            return self.price * (1 - self.discount / 100)
        return self.price
    