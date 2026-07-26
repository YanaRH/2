from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


# Обработчики для главной страницы и ошибок
def home(request):
    return TemplateView.as_view(template_name='home.html')(request)


def custom_404(request, exception):
    return TemplateView.as_view(
        template_name='404.html',
        status=404
    )(request)


def custom_500(request):
    return TemplateView.as_view(
        template_name='500.html',
        status=500
    )(request)


urlpatterns = [
    path('recipients/', views.recipient_list, name='recipient_list'),
    path('messages/', views.message_list, name='message_list'),
    path('', home, name='home'),
    path('users/', include('users.urls', namespace='users')),
    path('mailing/', include('mailing.urls', namespace='mailing')),
    path('admin/', admin.site.urls),

    # API endpoints (если есть)
    path('api/', include('api.urls', namespace='api')),
]

# Обработка ошибок
handler404 = custom_404
handler500 = custom_500

# Статические файлы в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

