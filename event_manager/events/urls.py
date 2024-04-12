from django.urls import path

from events import views

app_name = 'events'

urlpatterns = [
    path('create/', views.CreateEventView.as_view(), name='create'),
    path('add_part/', views.AddParticipantView.as_view(), name='add_part'),
    path('remove_part/',
         views.RemoveParticipantView.as_view(),
         name='remove_part',
         ),
]
