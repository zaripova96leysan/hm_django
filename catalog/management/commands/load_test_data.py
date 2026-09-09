from django.core.management.base import BaseCommand
from catalog.models import Category, Product

class Command(BaseCommand):
    help = 'Загружает тестовые данные (очищая таблицы)'

    def handle(self, *args, **options):
        # Очистка таблиц
        Category.objects.all().delete()
        Product.objects.all().delete()
        self.stdout.write('Данные очищены.')

        # Создание тестовых данных через ORM
        cat1 = Category.objects.create(name='Электроника', description='Гаджеты и техника')
        cat2 = Category.objects.create(name='Одежда', description='Модная одежда')
        Product.objects.create(name='Ноутбук', price=50000, category=cat1)
        Product.objects.create(name='Футболка', price=1500, category=cat2)

        self.stdout.write(self.style.SUCCESS('Тестовые данные загружены.'))