from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect


class AuthenticatedTradeMixin(UserPassesTestMixin):
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(
                self.request, "You are not allowed to modify other user's trades."
            )
            return redirect("trade_view")

        else:
            messages.info(self.request, "You must be logged in to modify a trade.")
            return redirect_to_login(
                self.request.get_full_path(),
                self.get_login_url(),
                self.get_redirect_field_name(),
            )

    def test_func(self):
        trade = self.get_object()
        return trade.username == self.request.user.username
