from django.db import models


class Trade(models.Model):
    INSTRUMENT_CHOICES = [
        ("bond", "Bond"),
        ("cds", "CDS"),
        ("futures", "Futures"),
        ("fx", "FX"),
    ]
    timestamp = models.DateTimeField(auto_now_add=True)
    trade_id = models.AutoField(primary_key=True)
    security_id = models.CharField(max_length=100)
    username = models.CharField(max_length=30)
    comment = models.CharField(max_length=150, blank=True)
    strategy = models.CharField(max_length=50)
    strategy_id = models.CharField(max_length=100)
    instrument_type = models.CharField(
        max_length=10, choices=INSTRUMENT_CHOICES, editable=False
    )

    def __str__(self):
        return f"Trade {self.trade_id} - {self.security_id} by {self.username}"


class BondTrade(Trade):
    price = models.FloatField()
    spread = models.FloatField()
    notional = models.FloatField()
    DIRECTION_CHOICES = [
        ("buy", "Buy"),
        ("sell", "Sell"),
    ]
    direction = models.CharField(max_length=4, choices=DIRECTION_CHOICES)

    def __str__(self):
        return f"BondTrade {self.trade_id} - {self.security_id}"


class CDSTrade(Trade):
    spread = models.FloatField()
    notional = models.FloatField()
    DIRECTION_CHOICES = [
        ("buy", "Buy"),
        ("sell", "Sell"),
    ]
    direction = models.CharField(max_length=4, choices=DIRECTION_CHOICES)

    def __str__(self):
        return f"CDSTrade {self.trade_id} - {self.security_id}"


class FuturesTrade(Trade):
    price = models.FloatField()
    no_of_contracts = models.IntegerField()
    DIRECTION_CHOICES = [
        ("buy", "Buy"),
        ("sell", "Sell"),
    ]
    direction = models.CharField(max_length=4, choices=DIRECTION_CHOICES)

    def __str__(self):
        return f"FuturesTrade {self.trade_id} - {self.security_id}"


class FXTrade(Trade):
    price = models.FloatField()
    notional = models.FloatField()
    DIRECTION_CHOICES = [
        ("buy", "Buy"),
        ("sell", "Sell"),
    ]
    direction = models.CharField(max_length=4, choices=DIRECTION_CHOICES)

    def __str__(self):
        return f"FXTrade {self.trade_id} - {self.security_id}"
