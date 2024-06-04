from django.shortcuts import redirect, render

from .forms import BondForm, CDSForm, FuturesForm, FXForm


def trade_view(request, type):
    if request.method == "POST":
        if type == "bond":  # maken into contants.PLEASE
            form = BondForm(request.POST)
        elif type == "cds":  # maken into contants.PLEASE
            form = CDSForm(request.POST)
        elif type == "fx":  # maken into contants.PLEASE
            form = FXForm(request.POST)
        elif type == "futures":  # maken into contants.PLEASE
            form = FuturesForm(request.POST)

        if form.is_valid():
            return redirect("success")
    else:
        if type == "bond":  # maken into contants.PLEASE
            form = BondForm()
        elif type == "cds":  # maken into contants.PLEASE
            form = CDSForm()
        elif type == "fx":  # maken into contants.PLEASE
            form = FXForm()
        elif type == "futures":  # maken into contants.PLEASE
            form = FuturesForm()
    return render(request, "trades/trade_view.html", {"type": type, "form": form})
