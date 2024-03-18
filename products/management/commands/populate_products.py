import csv
import logging
import random

from django.core.management import BaseCommand

from products.models import Products, Category, Brand
logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        apparel_brands = [
            "Nike",
            "Adidas",
            "Zara",
            "H&M (Hennes & Mauritz)",
            "GAP",
            "Levi's",
            "Under Armour",
            "Puma",
            "Ralph Lauren",
            "Tommy Hilfiger",
            "Calvin Klein",
            "Forever 21",
            "Hugo Boss",
            "Versace",
            "Armani"
        ]
        footwear_brands = [
            "Nike",
            "Adidas",
            "Puma",
            "Reebok",
            "Converse",
            "Vans",
            "New Balance",
            "Skechers",
            "Timberland",
            "Dr. Martens",
            "Under Armour",
            "ASICS",
            "Crocs",
            "Clarks",
            "Birkenstock"
        ]

        with open('fashion.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                try:
                    product_title = row['ProductTitle']
                    image_url = row['ImageURL']
                    price = random.randint(0,400)
                    category, created = Category.objects.get_or_create(title=row['SubCategory'])
                    product = Products()
                    product.category = category
                    if row['Category'] == 'Apparel':
                        brand, created = Brand.objects.get_or_create(title=random.choice(apparel_brands))
                        product.brand = brand
                    else:
                        brand, created = Brand.objects.get_or_create(title=random.choice(footwear_brands))
                        product.brand = brand

                    product.title = product_title
                    product.description = product_title
                    product.price = price
                    product.url = image_url
                    product.stock = 100
                    product.save()
                    count += 1
                except Exception as e:
                    pass
                finally:
                    logger.info(f"Added {count} products to database")

