from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("trade/", lambda request: redirect("trade_view", type="bonds", days_ago=10)),
    path("trade/<str:type>/<int:days_ago>", views.trade_view, name="trade_view"),
    path(
        "login/",
        LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "potential_trade/<int:pk>/",
        views.PotentialTradeUpdateView.as_view(),
        name="edit_potential_trade",
    ),
]
