def send_single_mailing(mailing_id):
    from .models import Mailing, MailingAttempt
    from django.utils import timezone
    from django.core.mail import send_mail
    from django.conf import settings

    mailing = Mailing.objects.get(pk=mailing_id)
    now = timezone.now()

    if not (mailing.start_time <= now <= mailing.end_time):
        # Если время не то — создаём попытки со статусом «Не успешно»
        for client in mailing.recipients.all():
            MailingAttempt.objects.create(
                mailing=mailing,
                recipient=client,
                status="Не успешно",
                server_response="Отправка вне временного окна",
            )
        return

    for client in mailing.recipients.all():
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[client.email],
                fail_silently=False,
            )
            status = "Успешно"
            response = "OK"
        except Exception as e:
            status = "Не успешно"
            response = str(e)

        MailingAttempt.objects.create(
            mailing=mailing,
            recipient=client,
            status=status,
            server_response=response,
        )
