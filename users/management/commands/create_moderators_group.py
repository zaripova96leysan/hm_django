from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Создаёт группу «Модератор продуктов» с нужными правами'

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name='Модератор продуктов')

        unpublish_permission = Permission.objects.get(codename='can_unpublish_product')
        delete_permission = Permission.objects.get(codename='delete_product')

        group.permissions.add(unpublish_permission, delete_permission)

        if created:
            self.stdout.write(self.style.SUCCESS('Группа «Модератор продуктов» создана'))
        else:
            self.stdout.write(self.style.SUCCESS('Группа «Модератор продуктов» уже существует, права обновлены'))