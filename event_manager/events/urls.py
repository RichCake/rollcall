from django.urls import path

from events import views

app_name = 'events'

urlpatterns = [
    path('create/', views.CreateEventView.as_view(), name='create'),
    path('<int:pk>/update/', views.UpdateEventView.as_view(), name='update'),
    path('<int:pk>/detail/', views.DetailEventView.as_view(), name='detail'),
    path('<int:pk>/delete/', views.DeleteEventView.as_view(), name='delete'),
    path('<int:pk>/attendance/', views.attendance_view, name='attendance'),
    path('add_part/', views.AddParticipantView.as_view(), name='add_part'),
    path(
        'remove_part/',
        views.RemoveParticipantView.as_view(),
        name='remove_part',
    ),
    path('list/', views.EventsListView.as_view(), name='list'),
]
