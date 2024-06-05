import json
from datetime import timedelta

from django.db.models import Count
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

from .constants import (
    TRADE_TYPE_BOND,
    TRADE_TYPE_CDS,
    TRADE_TYPE_FUTURES,
    TRADE_TYPE_FX,
)
from .forms import BondForm, CDSForm, FuturesForm, FXForm
from .models import PotentialTrade, Trade


def trade_view(request, type, days_ago):
    form = None
    potential_trades = PotentialTrade.objects.all()
    today = timezone.now()
    start_date = today - timedelta(days=days_ago)
    trades = Trade.objects.filter(trade_date__range=[start_date, today])
    trade_counts_qs = trades.values("instrument_type").annotate(count=Count("trade_id"))
    trade_counts_list = list(trade_counts_qs)
    trade_counts_json = json.dumps(trade_counts_list)
    # breakpoint()

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "add_trade":
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

        elif action == "finalise_trades":
            potential_trades = PotentialTrade.objects.all()
            for trade in potential_trades:
                trade_date = trade.trade_date
                security_id = trade.security_id
                username = trade.username
                comment = trade.comment
                strategy = trade.strategy
                strategy_id = trade.strategy_id
                instrument_type = trade.instrument_type
                price = trade.price
                spread = trade.spread
                notional = trade.notional
                direction = trade.direction
                no_of_contracts = trade.no_of_contracts

                Trade.objects.create(
                    trade_date=trade_date,
                    security_id=security_id,
                    username=username,
                    comment=comment,
                    strategy=strategy,
                    strategy_id=strategy_id,
                    instrument_type=instrument_type,
                    price=price,
                    spread=spread,
                    notional=notional,
                    direction=direction,
                    no_of_contracts=no_of_contracts,
                )

                trade.delete()
        return redirect(
            reverse(
                "trade_view",
                kwargs={
                    # "potential_trades": potential_trades,
                    # "trade_counts_json": trade_counts_json,
                    "type": type,
                    "days_ago": days_ago,
                    # "form": form,
                },
            )
        )

    else:
        if type == TRADE_TYPE_BOND:
            form = BondForm()
        elif type == TRADE_TYPE_CDS:
            form = CDSForm()
        elif type == TRADE_TYPE_FX:
            form = FXForm()
        elif type == TRADE_TYPE_FUTURES:
            form = FuturesForm()

    return render(
        request,
        "trades/trade_view.html",
        {
            "potential_trades": potential_trades,
            "trade_counts_json": trade_counts_json,
            "type": type,
            "days_ago": days_ago,
            "form": form,
        },
    )
