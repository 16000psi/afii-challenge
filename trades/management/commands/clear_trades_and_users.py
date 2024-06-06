from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from trades.models import (
    PotentialTrade,
    Trade,
)


class Command(BaseCommand):
    help = "Deletes all PotentialTrade and Trade instances, and deletes all non-superuser users"

    def handle(self, *args, **kwargs):
        self.delete_trades()
        self.delete_non_superusers()
        self.stdout.write(
            self.style.SUCCESS(
                "Successfully deleted all PotentialTrade and Trade instances, and all non-superuser users"
            )
        )

    def delete_trades(self):
        potential_trade_count = PotentialTrade.objects.count()
        trade_count = Trade.objects.count()

        PotentialTrade.objects.all().delete()
        Trade.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully deleted {potential_trade_count} PotentialTrade instances"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(f"Successfully deleted {trade_count} Trade instances")
        )

    def delete_non_superusers(self):
        non_superuser_count = User.objects.filter(is_superuser=False).count()
        User.objects.filter(is_superuser=False).delete()
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully deleted {non_superuser_count} non-superuser users"
            )
        )
