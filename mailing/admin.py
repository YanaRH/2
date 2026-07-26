from django.contrib import admin
from .models import Client, Message, Mailing, MailingAttempt

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'comment')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'body')

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('message', 'start_time', 'end_time', 'current_status')
    list_filter = ('start_time', 'end_time')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Если пользователь не суперпользователь, показываем только его рассылки.
        # Для простоты считаем, что рассылки привязаны к пользователю через поле user.
        if not request.user.is_superuser:
            qs = qs.filter(owner=request.user)
        return qs

@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'attempt_time', 'status')

