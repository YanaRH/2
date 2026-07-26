from django.shortcuts import render
from .models import Mailing, Client
from django.utils import timezone
from django.core.cache import cache


def dashboard(request):
    cache_key = 'dashboard_stats'
    stats = cache.get(cache_key)

    if stats is None:
        total_mailings = Mailing.objects.count()
        clients_count = Client.objects.count()
        now = timezone.now()
        active_mailings = Mailing.objects.filter(
            start_time__lte=now,
            end_time__gte=now
        ).count()
        stats = {
            'total_mailings': total_mailings,
            'active_mailings': active_mailings,
            'clients_count': clients_count
        }
        cache.set(cache_key, stats, 60)  # кэш на 60 секунд
    else:
        total_mailings = stats['total_mailings']
        active_mailings = stats['active_mailings']
        clients_count = stats['clients_count']

    context = {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'clients_count': clients_count,
    }
    return render(request, 'mailing/dashboard.html', context)

