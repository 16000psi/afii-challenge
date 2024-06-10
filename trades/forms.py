from django import forms
from django.forms import Textarea
from django.forms.widgets import DateInput, Select
from django.utils import timezone

from .models import PotentialTrade


class PotentialTradeForm(forms.ModelForm):
    class Meta:
        model = PotentialTrade
        fields = "__all__"
        widgets = {
            "trade_date": DateInput(attrs={"type": "date"}),
            "comment": Textarea(attrs={"rows": 2, "style": "resize: vertical;"}),
        }

    def __init__(self, *args, **kwargs):
        super(PotentialTradeForm, self).__init__(*args, **kwargs)
        self.fields["trade_date"].initial = timezone.now()
        self.order_fields(
            [
                "trade_date",
                "security_id",
                "strategy",
                "strategy_id",
                "price",
                "spread",
                "notional",
                "no_of_contracts",
                "direction",
                "comment",
            ]
        )


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

    def __init__(self, *args, **kwargs):
        super(BondForm, self).__init__(*args, **kwargs)
        self.order_fields(
            [
                "trade_date",
                "security_id",
                "strategy",
                "strategy_id",
                "price",
                "spread",
                "notional",
                "direction",
                "comment",
            ]
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

    def __init__(self, *args, **kwargs):
        super(CDSForm, self).__init__(*args, **kwargs)
        self.order_fields(
            [
                "trade_date",
                "security_id",
                "strategy",
                "strategy_id",
                "spread",
                "notional",
                "direction",
                "comment",
            ]
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

    def __init__(self, *args, **kwargs):
        super(FuturesForm, self).__init__(*args, **kwargs)
        self.order_fields(
            [
                "trade_date",
                "security_id",
                "strategy",
                "strategy_id",
                "price",
                "no_of_contracts",
                "direction",
                "comment",
            ]
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

    def __init__(self, *args, **kwargs):
        super(FXForm, self).__init__(*args, **kwargs)
        self.order_fields(
            [
                "trade_date",
                "security_id",
                "strategy",
                "strategy_id",
                "price",
                "notional",
                "direction",
                "comment",
            ]
        )
