from django.urls import path

from events import views

app_name = 'events'

urlpatterns = [
    path('create/', views.CreateEventView.as_view(), name='create'),
    path('<uuid:pk>/update/', views.UpdateEventView.as_view(), name='update'),
    path('<uuid:pk>/detail/', views.DetailEventView.as_view(), name='detail'),
    path('<uuid:pk>/participants_list/', views.EventParticipantsListView.as_view(), name='participants_list'),
    path('<uuid:pk>/delete/', views.DeleteEventView.as_view(), name='delete'),
    path('<uuid:pk>/attendance/', views.attendance_view, name='attendance'),
    path('send_request/', views.SendRequestView.as_view(), name='send_request'),
    path('revoke_request/', views.RevokeRequestView.as_view(), name='revoke_request'),
    path('accept_request/', views.AcceptRequestView.as_view(), name='accept_request'),
    path('list/', views.EventsListView.as_view(), name='list'),
]
