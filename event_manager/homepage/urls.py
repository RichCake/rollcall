from django.urls import path

from django.views.generic import TemplateView

app_name = "homepage"

urlpatterns = [
    path("", TemplateView.as_view(template_name="homepage/main.html"), name="home"),
    path("privacy/", TemplateView.as_view(template_name="privacy.html"), name="privacy"),
]
