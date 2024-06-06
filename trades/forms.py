from django import forms
from django.forms.widgets import DateInput, Select
from django.utils import timezone

from .models import PotentialTrade


class PotentialTradeForm(forms.ModelForm):
    class Meta:
        fields = "__all__"
        model = PotentialTrade
        widgets = {
            "trade_date": DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super(PotentialTradeForm, self).__init__(*args, **kwargs)
        self.fields["trade_date"].initial = timezone.now()


class BondForm(PotentialTradeForm):
    class Meta(PotentialTradeForm.Meta):
        exclude = ["no_of_contracts"]

    price = forms.FloatField(required=True)
    spread = forms.FloatField(required=True)
    notional = forms.FloatField(required=True)
    direction = forms.ChoiceField(
        choices=[("buy", "Buy"), ("sell", "Sell")], widget=Select(), required=True
    )
    strategy = forms.ChoiceField(
        choices=[
            ("active_short", "Active Short"),
            ("relval", "RelVal"),
            ("slbs", "SLBs"),
            ("curves", "Curves"),
            ("use_of_proceeds", "Use of Proceeds"),
            ("", "--"),
        ],
        widget=Select(),
        required=False,
    )


class CDSForm(PotentialTradeForm):
    class Meta(PotentialTradeForm.Meta):
        exclude = ["price", "no_of_contracts"]

    spread = forms.FloatField(required=True)
    notional = forms.FloatField(required=True)
    direction = forms.ChoiceField(
        choices=[("buy", "Buy"), ("sell", "Sell")], widget=Select(), required=True
    )
    strategy = forms.ChoiceField(
        choices=[
            ("active_short", "Active Short"),
            ("relval", "RelVal"),
            ("slbs", "SLBs"),
            ("curves", "Curves"),
            ("use_of_proceeds", "Use of Proceeds"),
            ("", "--"),
        ],
        widget=Select(),
        required=False,
    )


class FuturesForm(PotentialTradeForm):
    class Meta(PotentialTradeForm.Meta):
        exclude = ["spread", "notional"]

    price = forms.FloatField(required=True)
    no_of_contracts = forms.IntegerField(required=True)
    direction = forms.ChoiceField(
        choices=[("buy", "Buy"), ("sell", "Sell")], widget=Select(), required=True
    )
    strategy = forms.ChoiceField(
        choices=[
            ("hedge", "Hedge"),
            ("", "--"),
        ],
        widget=Select(),
        required=False,
    )


class FXForm(PotentialTradeForm):
    class Meta(PotentialTradeForm.Meta):
        exclude = ["spread", "no_of_contracts"]

    price = forms.FloatField(required=True)
    notional = forms.FloatField(required=True)
    direction = forms.ChoiceField(
        choices=[("buy", "Buy"), ("sell", "Sell")], widget=Select(), required=True
    )
    strategy = forms.ChoiceField(
        choices=[
            ("hedge", "Hedge"),
            ("", "--"),
        ],
        widget=Select(),
        required=False,
    )
