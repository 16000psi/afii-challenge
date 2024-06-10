import pandas as pd
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import UpdateView

from .constants import (
    TRADE_TYPE_BOND,
    TRADE_TYPE_CDS,
    TRADE_TYPE_FUTURES,
    TRADE_TYPE_FX,
)
from .forms import BondForm, CDSForm, FuturesForm, FXForm, PotentialTradeForm
from .mixins import AuthenticatedTradeMixin
from .models import PotentialTrade, Trade


@login_required
def trade_view(request):
    form = None
    potential_trades = PotentialTrade.objects.filter(
        username=request.user.username
    ).order_by("trade_date")

    paginator = Paginator(potential_trades, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if request.method == "POST":
        instrument_type = request.POST.get("trade_type")
        action = request.POST.get("action")

        form_classes = {
            TRADE_TYPE_BOND: BondForm,
            TRADE_TYPE_CDS: CDSForm,
            TRADE_TYPE_FX: FXForm,
            TRADE_TYPE_FUTURES: FuturesForm,
        }

        if action == "add_trade":
            form_class = form_classes.get(instrument_type)
            if form_class:
                form = form_class(request.POST)
                if form.is_valid():
                    potential_trade = form.save(commit=False)
                    potential_trade.instrument_type = instrument_type
                    potential_trade.username = request.user.username
                    potential_trade.save()
                    messages.success(request, "Trade added successfully.")
                    return redirect("trade_view")
                else:
                    messages.error(
                        request,
                        "The trade could not be added. Please check the form for errors.",
                    )
            else:
                messages.error(request, "Invalid instrument type selected.")

        elif action == "finalise_trades":
            trade_data_list = [
                Trade(
                    trade_date=trade.trade_date,
                    security_id=trade.security_id,
                    username=trade.username,
                    comment=trade.comment,
                    strategy=trade.strategy,
                    strategy_id=trade.strategy_id,
                    instrument_type=trade.instrument_type,
                    price=trade.price,
                    spread=trade.spread,
                    notional=trade.notional,
                    direction=trade.direction,
                    no_of_contracts=trade.no_of_contracts,
                )
                for trade in potential_trades
            ]
            Trade.objects.bulk_create(trade_data_list)
            potential_trades.delete()
            messages.success(request, "Trades uploaded successfully.")
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


class PotentialTradeUpdateView(AuthenticatedTradeMixin, UpdateView):
    model = PotentialTrade
    template_name = "trades/potential_trade_form.html"
    context_object_name = "trade"
    success_url = reverse_lazy("trade_view")

    def get_form_class(self):
        form_classes = {
            TRADE_TYPE_BOND: BondForm,
            TRADE_TYPE_CDS: CDSForm,
            TRADE_TYPE_FUTURES: FuturesForm,
            TRADE_TYPE_FX: FXForm,
        }
        return form_classes.get(self.get_object().instrument_type)

    def form_valid(self, form):
        messages.success(self.request, "Trade saved successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "The trade could not be updated. Please check the form for errors.",
        )
        return super().form_invalid(form)


@login_required
def delete_potential_trade(request, pk):
    potential_trade = get_object_or_404(PotentialTrade, pk=pk)
    if request.user.username == potential_trade.username:
        potential_trade.delete()
        messages.success(request, "Trade deleted successfully.")
        return redirect(reverse_lazy("trade_view"))
    else:
        return HttpResponseForbidden("You are not allowed to delete this trade.")


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("trade_view")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Account created successfully. Please log in.")
        return response


def get_trade_counts(request, days_ago, parameter):
    if request.method == "GET":
        try:
            trade_counts = Trade.objects.get_trade_counts(days_ago, parameter)
            trade_data = list(trade_counts)
            return JsonResponse(trade_data, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


def get_type_counts(request, days_ago, instrument_type, metric):
    if request.method == "GET":
        try:
            trades = Trade.objects.filter_by_date_range(days_ago).filter(
                instrument_type=instrument_type
            )
            data = list(trades.values("trade_id", metric))
            df = pd.DataFrame(data)

            if df.empty:
                return JsonResponse([], safe=False)

            df[metric] = df[metric].round(0).astype(int)
            df["price_bin"] = pd.cut(df[metric], bins=8)
            grouped = df.groupby("price_bin", observed=False)
            price_distribution = [
                {
                    "price_bin": f"{int(bin_label.left)}-{int(bin_label.right)}",
                    "count": len(bin_group),
                }
                for bin_label, bin_group in grouped
            ]

            return JsonResponse(price_distribution, safe=False)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
