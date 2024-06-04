from django import forms

from .models import Trade


class TradeForm(forms.ModelForm):
    class Meta:
        model = Trade
        fields = "__all__"


class BondForm(TradeForm):
    bond_extra = forms.CharField(max_length=10, label="bond")


class CDSForm(TradeForm):
    cds_extra = forms.CharField(max_length=10, label="cds")


class FXForm(TradeForm):
    fx_extra = forms.CharField(max_length=10, label="fx")


class FuturesForm(TradeForm):
    futures_extra = forms.CharField(max_length=10, label="futures")
