from django.urls import path

from . import views

urlpatterns = [
    path("<str:type>", views.trade_view, name="trade_view"),
]
