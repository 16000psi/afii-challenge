from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from django.views.generic.edit import UpdateView

from .constants import (
    TRADE_TYPE_BOND,
    TRADE_TYPE_CDS,
    TRADE_TYPE_FUTURES,
    TRADE_TYPE_FX,
)
from .forms import BondForm, CDSForm, FuturesForm, FXForm, PotentialTradeForm
from .models import PotentialTrade, Trade


@login_required
def trade_view(request):
    form = None
    potential_trades = PotentialTrade.objects.filter(username=request.user.username)

    paginator = Paginator(potential_trades, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if request.method == "POST":
        instrument_type = request.POST.get("trade_type")
        action = request.POST.get("action")
        if action == "add_trade":
            if instrument_type == TRADE_TYPE_BOND:
                form = BondForm(request.POST)
            elif instrument_type == TRADE_TYPE_CDS:
                form = CDSForm(request.POST)
            elif instrument_type == TRADE_TYPE_FX:
                form = FXForm(request.POST)
            elif instrument_type == TRADE_TYPE_FUTURES:
                form = FuturesForm(request.POST)

            if form.is_valid():
                potential_trade = form.save(commit=False)
                potential_trade.instrument_type = instrument_type
                potential_trade.username = request.user.username
                potential_trade.save()

        elif action == "finalise_trades":
            for trade in potential_trades:
                trade_data = {
                    "trade_date": trade.trade_date,
                    "security_id": trade.security_id,
                    "username": trade.username,
                    "comment": trade.comment,
                    "strategy": trade.strategy,
                    "strategy_id": trade.strategy_id,
                    "instrument_type": trade.instrument_type,
                    "price": trade.price,
                    "spread": trade.spread,
                    "notional": trade.notional,
                    "direction": trade.direction,
                    "no_of_contracts": trade.no_of_contracts,
                }

                Trade.objects.create(**trade_data)
                trade.delete()
        return redirect("trade_view")

    else:
        form = PotentialTradeForm()

    return render(
        request,
        "trades/trade_view.html",
        {
            "potential_trades": page_obj,
            "form": form,
        },
    )


class PotentialTradeUpdateView(UpdateView):
    model = PotentialTrade
    template_name = "trades/potential_trade_form.html"
    context_object_name = "trade"
    success_url = reverse_lazy("trade_view")

    def get_form_class(self):
        potential_trade = self.get_object()
        if potential_trade.instrument_type == "bond":
            return BondForm
        elif potential_trade.instrument_type == "cds":
            return CDSForm
        elif potential_trade.instrument_type == "futures":
            return FuturesForm
        elif potential_trade.instrument_type == "fx":
            return FXForm

    def dispatch(self, request, *args, **kwargs):
        potential_trade = self.get_object()
        if request.user.username != potential_trade.username:
            return HttpResponseForbidden("You are not allowed to edit this trade.")
        return super().dispatch(request, *args, **kwargs)


@login_required
def delete_potential_trade(request, pk):
    potential_trade = get_object_or_404(PotentialTrade, pk=pk)
    if request.user.username == potential_trade.username:
        potential_trade.delete()
        return redirect(reverse_lazy("trade_view"))
    else:
        return HttpResponseForbidden("You are not allowed to delete this trade.")


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("trade_view")
    template_name = "registration/signup.html"


def get_trade_counts(request, days_ago, parameter):
    if request.method == "GET":
        today = timezone.now()
        start_date = today - timedelta(days=days_ago)
        trades = Trade.objects.filter(trade_date__range=[start_date, today])
        trade_counts_qs = trades.values(parameter).annotate(
            count=Count("trade_id")
        )
        trade_data = list(trade_counts_qs)
        return JsonResponse(trade_data, safe=False)
