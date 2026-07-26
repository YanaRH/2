from django.core.mail import send_mail
from django.conf import settings
from .models import Mailing, MailingAttempt
from django.utils import timezone

def send_mailing(mailing_id):
    """
    Отправка рассылки по ID.
    Проверяет статус, отправляет письма каждому клиенту, логирует результат.
    """
    mailing = Mailing.objects.get(id=mailing_id)
    now = timezone.now()

    # Проверка временного окна
    if not (mailing.start_time <= now <= mailing.end_time):
        return "Ошибка: отправка вне временного окна."

    if mailing.current_status != "Запущена":
        return "Ошибка: рассылка не в статусе 'Запущена'."

    success_count = 0
    fail_count = 0

    for client in mailing.recipients.all():
        try:
            # Здесь реальная отправка. Если SMTP не настроен — будет ошибка,
            # но логика и журнал всё равно работают.
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[client.email],
                fail_silently=False,
            )
            status = "Успешно"
            success_count += 1
        except Exception as e:
            status = "Не успешно"
            fail_count += 1
            server_response_text = str(e)
        else:
            server_response_text = "OK"

        # Создаём запись в журнале
        MailingAttempt.objects.create(
            mailing=mailing,
            status=status,
            server_response=server_response_text,
        )

    return f"Отправлено: {success_count}, ошибок: {fail_count}"
