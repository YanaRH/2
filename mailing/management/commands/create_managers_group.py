from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Создает группу "Менеджеры" с необходимыми разрешениями'

    def handle(self, *args, **options):
        group_name = "Менеджеры"
        group, created = Group.objects.get_or_create(name=group_name)

        if created:
            self.stdout.write(self.style.SUCCESS(f'Группа "{group_name}" создана.'))
        else:
            self.stdout.write(
                self.style.WARNING(f'Группа "{group_name}" уже существует.')
            )

        permission_codenames = [
            "view_client_list",
            "view_message_list",
            "set_mailing_status",
            "view_mailing_list",
        ]

        permissions_to_add = []
        for codename in permission_codenames:
            try:
                perm = Permission.objects.get(codename=codename)
                permissions_to_add.append(perm)
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Разрешение "{codename}" не найдено.')
                )

        for perm in permissions_to_add:
            group.permissions.add(perm)

        if permissions_to_add:
            self.stdout.write(
                self.style.SUCCESS(f'Добавлены разрешения в группу "{group_name}".')
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f'Не найдено разрешений для добавления в группу "{group_name}".'
                )
            )
