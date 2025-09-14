from django.urls import path
from . import views

urlpatterns = [
    path("site/by-host/<str:host>", views.site_by_host, name="site_by_host"),
    path("site/<int:site_id>/switch-template", views.switch_template, name="switch_template"),
]
