from django.core.exceptions import ValidationError
from django.db import models


class BaseTrade(models.Model):
    INSTRUMENT_CHOICES = [
        ("bond", "Bond"),
        ("cds", "CDS"),
        ("futures", "Futures"),
        ("fx", "FX"),
    ]
    STRATEGY_CHOICES = [
        ("active_short", "Active Short"),
        ("relval", "RelVal"),
        ("slbs", "SLBs"),
        ("curves", "Curves"),
        ("use_of_proceeds", "Use of Proceeds"),
        ("hedge", "Hedge"),
    ]
    trade_date = models.DateTimeField()  # needs to be just date
    trade_id = models.AutoField(primary_key=True)
    security_id = models.CharField(max_length=100)
    username = models.CharField(max_length=150, editable=False)
    comment = models.CharField(max_length=150, blank=True)
    strategy = models.CharField(
        choices=STRATEGY_CHOICES, max_length=15, blank=True, null=True
    )
    strategy_id = models.CharField(max_length=100)
    instrument_type = models.CharField(
        max_length=10, choices=INSTRUMENT_CHOICES, editable=False
    )

    price = models.FloatField(null=True, blank=True)
    spread = models.FloatField(null=True, blank=True)
    notional = models.FloatField(null=True, blank=True)
    DIRECTION_CHOICES = [
        ("buy", "Buy"),
        ("sell", "Sell"),
    ]
    direction = models.CharField(
        null=True, blank=True, max_length=4, choices=DIRECTION_CHOICES
    )
    no_of_contracts = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True

    def clean(self):
        super().clean()
        instrument_type = self.instrument_type

        required_fields = {
            "bond": ["price", "spread", "notional", "direction"],
            "cds": ["spread", "notional", "direction"],
            "futures": ["price", "no_of_contracts", "direction"],
            "fx": ["price", "notional", "direction"],
        }

        # Get the required fields for the current instrument type
        required_fields_for_instrument = required_fields.get(instrument_type, [])

        # Check if all required fields are present
        errors = {}
        for field in required_fields_for_instrument:
            if getattr(self, field) in [None, ""]:
                errors[field] = _(
                    f"This field is required for {instrument_type} trades."
                )

        if errors:
            raise ValidationError(errors)


class PotentialTrade(BaseTrade):
    def __str__(self):
        return f"Potential {self.instrument_type} trade {self.trade_id} - {self.security_id} by {self.username}"


class Trade(BaseTrade):
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Committed  {self.instrument_type} trade {self.trade_id} - {self.security_id} by {self.username}"
