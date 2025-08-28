from django.urls import path

from notifications import views

app_name = 'notifications'

urlpatterns = [
    path('link_telegram_user/', views.link_telegram_user, name='link_tg'),
]
