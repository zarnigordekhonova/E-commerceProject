# management/commands/populate_fake_data.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from decimal import Decimal
import random
from datetime import datetime, timedelta

from apps.accounts.models import CustomUser, UserDeliveryAddres
from apps.common.models import Country, City, Designer, NewsLetter
from apps.products.models import (
    Category, Product, ProductVariant, Option, OptionValue,
    ProductVariantOptionValue, ProductRating, ProductComment, 
    UserProductFavorite, ProductImage
)
from apps.orders.models import Order, OrderItem
from apps.blog.models import Post  # Adjust import if needed

fake = Faker()
User = get_user_model()


class Command(BaseCommand):
    help = 'Populate database with fake data for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=5,
            help='Number of users to create'
        )
        parser.add_argument(
            '--products',
            type=int,
            default=10,
            help='Number of products to create'
        )
        parser.add_argument(
            '--orders',
            type=int,
            default=5,
            help='Number of orders to create'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to populate fake data...'))
        
        # Create common data
        self.create_countries_and_cities()
        self.create_designers()
        
        # Create main data
        self.create_users(options['users'])
        self.create_categories()
        self.create_options()
        self.create_products(options['products'])
        self.create_products_images()
        self.create_ratings_and_comments()
        self.create_favorites()
        self.create_orders(options['orders'])
        self.create_newsletter()
        
        self.stdout.write(self.style.SUCCESS('Successfully populated fake data!'))

    def create_countries_and_cities(self):
        self.stdout.write('Creating countries and cities...')
        
        countries_data = [
            {'name': 'Uzbekistan', 'code': 'UZ'},
            {'name': 'Kazakhstan', 'code': 'KZ'},
            {'name': 'Tajikistan', 'code': 'TJ'},
            {'name': 'Turkmenistan', 'code': 'TM'},
        ]
        
        for country_data in countries_data:
            country, _ = Country.objects.get_or_create(**country_data)
            
            # Create cities for each country
            cities = [fake.city() for _ in range(3)]
            for city_name in cities:
                City.objects.get_or_create(
                    name=city_name,
                    country=country
                )

    def create_designers(self):
        self.stdout.write('Creating designers...')
        
        designers = ['John Designer', 'Sarah Architect', 'Mike Creator', 'Emma Sculptor']
        for designer_name in designers:
            Designer.objects.get_or_create(full_name=designer_name)

    def create_users(self, count):
        self.stdout.write(f'Creating {count} users...')
        
        for i in range(count):
            username = f'user_{i}_{fake.user_name()}'[:50]
            email = f'user_{i}_{fake.email()}'
            
            user, created = CustomUser.objects.get_or_create(
                email=email,
                defaults={
                    'username': username,
                    'full_name': fake.name(),
                    'is_active': True,
                    'is_confirmed': True,
                }
            )
            
            if created:
                user.set_password('testpass123')
                user.save()
                
                # Create delivery addresses
                country = Country.objects.order_by('?').first()
                city = City.objects.filter(country=country).first()
                
                if country and city:
                    UserDeliveryAddres.objects.create(
                        user=user,
                        country=country,
                        city=city,
                        street=fake.street_address(),
                        building_number=fake.building_number(),
                        is_default=True
                    )

    def create_categories(self):
        self.stdout.write('Creating categories...')
        
        categories = ['Electronics', 'Furniture', 'Clothing', 'Books', 'Sports']
        for category_name in categories:
            Category.objects.get_or_create(category_name=category_name)

    def create_options(self):
        self.stdout.write('Creating options and values...')
        
        options_data = {
            'color': ['red', 'blue', 'green', 'black', 'white'],
            'size': ['small', 'medium', 'large', 'xl'],
            'material': ['cotton', 'wool', 'silk', 'polyester'],
        }
        
        for option_name, values in options_data.items():
            option, _ = Option.objects.get_or_create(name=option_name)
            
            for value in values:
                OptionValue.objects.get_or_create(
                    option=option,
                    value=value
                )

    def create_products(self, count):
        self.stdout.write(f'Creating {count} products...')
        
        for i in range(count):
            category = Category.objects.order_by('?').first()
            designer = Designer.objects.order_by('?').first()
            
            product = Product.objects.create(
                name=fake.word() + ' ' + str(i),
                description=fake.text(),
                rating=round(random.uniform(0, 5), 2),
                is_new=random.choice([True, False]),
                designed_by=designer,
                category=category,
                show_with_posts=random.choice([True, False])
            )
            
            # Create variants for each product
            for j in range(random.randint(1, 3)):
                variant = ProductVariant.objects.create(
                    product=product,
                    sku_code=f'SKU_{product.id}_{j}_{fake.bothify()}',
                    stock_quantity=random.randint(5, 100),
                    price=Decimal(str(round(random.uniform(10, 500), 2))),
                    discount_percentage=random.choice([0, 5, 10, 15, 20]),
                    additional_info=fake.text(max_nb_chars=100)
                )
                
                # Create ProductVariantOptionValue
                options = Option.objects.all()[:random.randint(1, 2)]
                for option in options:
                    option_value = OptionValue.objects.filter(option=option).order_by('?').first()
                    if option_value:
                        ProductVariantOptionValue.objects.get_or_create(
                            product_variant=variant,
                            option_value=option_value
                        )

    def create_products_images(self):
        self.stdout.write('Creating product images...')
        
        from django.core.files.base import ContentFile
        
        variants = ProductVariant.objects.all()
        
        for variant in variants[:10]:  # Create images for first 10 variants
            # Create a simple placeholder image
            image_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
            
            ProductImage.objects.create(
                product=variant,
                image=ContentFile(image_content, name=f'product_{variant.id}.png')
            )

    def create_ratings_and_comments(self):
        self.stdout.write('Creating ratings and comments...')
        
        users = CustomUser.objects.all()
        products = Product.objects.all()
        
        for product in products[:5]:
            for user in users[:3]:
                # Create rating
                ProductRating.objects.get_or_create(
                    user=user,
                    product=product,
                    defaults={
                        'rating': round(random.uniform(1, 5), 1)
                    }
                )
                
                # Create comment
                ProductComment.objects.create(
                    user=user,
                    product=product,
                    comment=fake.text(max_nb_chars=200)
                )

    def create_favorites(self):
        self.stdout.write('Creating favorites...')
        
        users = CustomUser.objects.all()
        variants = ProductVariant.objects.all()
        
        for user in users:
            for variant in variants[:random.randint(1, 3)]:
                UserProductFavorite.objects.get_or_create(
                    user=user,
                    product=variant
                )

    def create_orders(self, count):
        self.stdout.write(f'Creating {count} orders...')
        
        users = CustomUser.objects.all()
        variants = ProductVariant.objects.all()
        countries = Country.objects.all()
        cities = City.objects.all()
        
        for i in range(count):
            user = random.choice(users)
            country = random.choice(countries)
            city = random.choice(cities.filter(country=country))
            
            order = Order.objects.create(
                user=user,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone_number='+998' + ''.join([str(random.randint(0, 9)) for _ in range(9)]),
                email=user.email,
                country=country,
                city=city,
                state=fake.state(),
                street=fake.street_address(),
                zip_code=fake.postcode(),
                payment_method=random.choice(['CREDIT_CARD', 'PAYPAL', 'CASH_ON_DELIVERY']),
                shipping_type=random.choice(['FREE', 'EXPRESS', 'PICKUP']),
                shipping_cost=Decimal('0.00') if random.choice([True, False]) else Decimal('15.00'),
                status=random.choice(['PENDING', 'PROCESSING', 'SHIPPING', 'DELIVERED']),
                total_price=Decimal(str(round(random.uniform(100, 1000), 2)))
            )
            
            # Create order items
            for _ in range(random.randint(1, 3)):
                variant = random.choice(variants)
                OrderItem.objects.create(
                    order=order,
                    product=variant,
                    quantity=random.randint(1, 5),
                    price=variant.price
                )

    def create_newsletter(self):
        self.stdout.write('Creating newsletter subscribers...')
        
        for i in range(5):
            NewsLetter.objects.get_or_create(
                email=f'newsletter_{i}_{fake.email()}'
            )