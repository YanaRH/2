from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Добавляет пользователя в группу "Менеджеры"'

    def add_arguments(self, parser):
        parser.add_argument("username", type=str, help="Имя пользователя")

    def handle(self, *args, **options):
        username = options["username"]
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Пользователь "{username}" не найден.'))
            return

        try:
            managers_group = Group.objects.get(name="Менеджеры")
        except Group.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Группа "Менеджеры" не найдена. Создайте её сначала.')
            )
            return

        if managers_group in user.groups.all():
            self.stdout.write(
                self.style.WARNING(
                    f'Пользователь "{username}" уже состоит в группе "Менеджеры".'
                )
            )
        else:
            user.groups.add(managers_group)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Пользователь "{username}" добавлен в группу "Менеджеры".'
                )
            )
