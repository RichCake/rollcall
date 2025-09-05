from django.urls import path
from django.views.decorators.cache import cache_page

from profiles import views

app_name = "profiles"

urlpatterns = [
    path("list/", views.UserListView.as_view(), name="list"),
    path(
        "detail/<uuid:pk>/",
        cache_page(60 * 5)(views.UserDetailView.as_view()),
        name="detail",
    ),
    path("update/<uuid:pk>/", views.UserUpdateView.as_view(), name="update"),
]
