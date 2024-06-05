from django.shortcuts import redirect
from django.urls import path

from . import views

urlpatterns = [
    path("trade/", lambda request: redirect("trade_view", type="bonds", days_ago=10)),
    path("trade/<str:type>/<int:days_ago>", views.trade_view, name="trade_view"),
]
