from django.shortcuts import redirect, render
from django.urls import reverse

from .constants import (
    TRADE_TYPE_BOND,
    TRADE_TYPE_CDS,
    TRADE_TYPE_FUTURES,
    TRADE_TYPE_FX,
)
from .forms import BondForm, CDSForm, FuturesForm, FXForm
from .models import PotentialTrade


def trade_view(request, type):
    form = None
    if request.method == "POST":
        if type == TRADE_TYPE_BOND:
            form = BondForm(request.POST)
        elif type == TRADE_TYPE_CDS:
            form = CDSForm(request.POST)
        elif type == TRADE_TYPE_FX:
            form = FXForm(request.POST)
        elif type == TRADE_TYPE_FUTURES:
            form = FuturesForm(request.POST)

        if form.is_valid():
            potential_trade = form.save(commit=False)
            potential_trade.instrument_type = type
            potential_trade.save()
            return redirect(reverse('trade_view', kwargs={'type': type}))

    else:
        if type == TRADE_TYPE_BOND:
            form = BondForm()
        elif type == TRADE_TYPE_CDS:
            form = CDSForm()
        elif type == TRADE_TYPE_FX:
            form = FXForm()
        elif type == TRADE_TYPE_FUTURES:
            form = FuturesForm()
    return render(request, "trades/trade_view.html", {"type": type, "form": form})
