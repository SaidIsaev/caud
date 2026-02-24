import os, django, csv
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shoestore.settings')
django.setup()

from products.models import Category, Manufacturer, Supplier, Product

with open('data/Tovar.csv', 'r', encoding='utf-8-sig') as f:
    for r in csv.DictReader(f, delimiter=';'):
        
        cat, _ = Category.objects.get_or_create(name=r['Категория товара'].strip())
        man, _ = Manufacturer.objects.get_or_create(name=r['Производитель'].strip())
        sup, _ = Supplier.objects.get_or_create(name=r['Поставщик'].strip())
        
        price_str = r['Цена'].strip().replace(',', '.')
        price_val = Decimal(price_str) if price_str else Decimal('0')
        
        discount_str = r['Действующая скидка'].strip().replace(',', '.')
        discount_val = Decimal(discount_str) if discount_str else Decimal('0')
        
        stock_val = int(r['Кол-во на складе'].strip()) if r['Кол-во на складе'].strip() else 0
        
        Product.objects.get_or_create(
            SKU=r['Артикул'].strip(),
            defaults={
                'name': r['Наименование товара'].strip(),
                'category': cat,
                'manufacturer': man,
                'supplier': sup,
                'description': r['Описание товара'].strip(),
                'unit_type': r['Единица измерения'].strip(),
                'price': price_val,
                'discount': discount_val,
                'stock_quantity': stock_val,
                'image': r['Фото'].strip() if r['Фото'].strip() else None, 
            }
        )
        print(f"✓ {r['Артикул']}: {r['Наименование товара']}")

print(f"\n✓ Всего товаров: {Product.objects.count()}")