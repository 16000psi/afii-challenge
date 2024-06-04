from django.contrib import admin

from .models import BondTrade, CDSTrade, FuturesTrade, FXTrade


class TradeAdmin(admin.ModelAdmin):
    readonly_fields = ("timestamp",)


class BondTradeAdmin(TradeAdmin):
    list_display = (
        "trade_id",
        "security_id",
        "username",
        "timestamp",
        "price",
        "spread",
        "notional",
        "direction",
    )


class CDSTradeAdmin(TradeAdmin):
    list_display = (
        "trade_id",
        "security_id",
        "username",
        "timestamp",
        "spread",
        "notional",
        "direction",
    )


class FuturesTradeAdmin(TradeAdmin):
    list_display = (
        "trade_id",
        "security_id",
        "username",
        "timestamp",
        "price",
        "no_of_contracts",
        "direction",
    )


class FXTradeAdmin(TradeAdmin):
    list_display = (
        "trade_id",
        "security_id",
        "username",
        "timestamp",
        "price",
        "notional",
        "direction",
    )


admin.site.register(BondTrade, BondTradeAdmin)
admin.site.register(CDSTrade, CDSTradeAdmin)
admin.site.register(FuturesTrade, FuturesTradeAdmin)
admin.site.register(FXTrade, FXTradeAdmin)
