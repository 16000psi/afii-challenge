from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("trade/", views.trade_view, name="trade_view"),
    path(
        "login/",
        LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "potential_trade/<int:pk>/",
        views.PotentialTradeUpdateView.as_view(),
        name="potential_trade_edit",
    ),
    path(
        "potential_trade/<int:pk>/delete/",
        views.delete_potential_trade,
        name="potential_trade_delete",
    ),
    path(
        "trade_counts/<int:days_ago>/<str:parameter>/",
        views.get_trade_counts,
        name="get_trade_counts",
    ),
    path(
        "type_chart/<int:days_ago>/<str:instrument_type>/<str:metric>/",
        views.get_type_counts,
        name="get_type_counts",
    ),
    path("", RedirectView.as_view(url="/trade/", permanent=True)),
]
