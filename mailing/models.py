from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User


class Client(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.full_name} ({self.email})"


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    # Сначала owner, чтобы админка могла фильтровать
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mailings')

    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Client, related_name='mailings')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    @property
    def current_status(self):
        now = timezone.now()
        if now < self.start_time:
            return "Создана"
        elif now <= self.end_time:
            return "Запущена"
        else:
            return "Завершена"

    def clean(self):
        super().clean()
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                raise ValidationError("Дата начала должна быть раньше даты окончания.")
            if self.start_time < timezone.now():
                raise ValidationError("Дата начала не может быть в прошлом.")

    def __str__(self):
        return f"Рассылка: {self.message.subject} — {self.current_status}"


class MailingAttempt(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='attempts')
    attempt_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ('Успешно', 'Успешно'),
            ('Не успешно', 'Не успешно'),
        ]
    )
    server_response = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.mailing.id} — {self.status} at {self.attempt_time}"
