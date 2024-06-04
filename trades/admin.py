from django.contrib import admin

from .models import PotentialTrade, Trade


class TradeAdmin(admin.ModelAdmin):
    readonly_fields = ("timestamp",)


admin.site.register(Trade, TradeAdmin)
admin.site.register(PotentialTrade)
