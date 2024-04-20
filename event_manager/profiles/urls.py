from django.urls import path

from profiles import views

app_name = 'profiles'

urlpatterns = [
    path('list/', views.UserListView.as_view(), name='list'),
    path('detail/<int:pk>/', views.UserDetailView.as_view(), name='detail'),
]
