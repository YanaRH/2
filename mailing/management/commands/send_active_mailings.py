from django.core.management.base import BaseCommand
from django.utils import timezone

from mailing.models import Mailing
from mailing.services import send_mailing


class Command(BaseCommand):
    help = "Отправляет активные рассылки, время которых наступило"

    def handle(self, *args, **options):
        now = timezone.now()
        mailings_to_send = Mailing.objects.filter(
            status="running", first_send_time__lte=now, end_time__gte=now
        )

        if not mailings_to_send.exists():
            self.stdout.write(self.style.WARNING("Нет активных рассылок для отправки."))
            return

        self.stdout.write(f"Найдено рассылок для отправки: {mailings_to_send.count()}")

        for mailing in mailings_to_send:
            self.stdout.write(f"Отправка рассылки ID: {mailing.id}")
            success = send_mailing(mailing.id)
            if success:
                self.stdout.write(
                    self.style.SUCCESS(f"Рассылка ID {mailing.id} отправлена.")
                )

                if mailing.status == "created":
                    mailing.status = "running"
                    mailing.save()
            else:
                self.stdout.write(
                    self.style.ERROR(f"Ошибка при отправке рассылки ID {mailing.id}.")
                )

        self.stdout.write(self.style.SUCCESS("Процесс отправки рассылок завершен."))
