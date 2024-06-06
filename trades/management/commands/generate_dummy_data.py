import random
from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from trades.models import Trade  # Adjust the import based on your app name


class Command(BaseCommand):
    help = "Populates the database with Trades"

    def handle(self, *args, **kwargs):
        self.create_users()
        self.create_trades()

    def create_users(self):
        self.users = []
        for i in range(10):
            username = f"user_{i+1}"
            user = User.objects.create_user(username=username, password="password")
            self.users.append(user)

    def create_random_date(self):
        start_date = timezone.now() - timedelta(days=3 * 365)
        end_date = timezone.now()
        return start_date + (end_date - start_date) * random.random()

    def create_trades(self):
        STRATEGY_CHOICES_BONDS_CDS = [
            "active_short",
            "relval",
            "slbs",
            "curves",
            "use_of_proceeds",
        ]

        # Generate bonds
        for _ in range(50):
            trade = Trade(
                trade_date=self.create_random_date(),
                security_id=f"security_{random.randint(1000, 9999)}",
                username=random.choice(self.users).username,
                instrument_type="bond",
                strategy_id=f"strategy_{random.randint(100, 999)}",
                strategy=random.choice(STRATEGY_CHOICES_BONDS_CDS),
                price=random.uniform(1, 500),
                spread=random.uniform(1, 500),
                notional=random.randint(1, 100000000),
                direction=random.choice(["buy", "sell"]),
            )
            trade.clean()
            trade.save()

        # Generate CDS
        for _ in range(50):
            trade = Trade(
                trade_date=self.create_random_date(),
                security_id=f"security_{random.randint(1000, 9999)}",
                username=random.choice(self.users).username,
                instrument_type="cds",
                strategy_id=f"strategy_{random.randint(100, 999)}",
                strategy=random.choice(STRATEGY_CHOICES_BONDS_CDS),
                spread=random.uniform(1, 500),
                notional=random.randint(1, 100000000),
                direction=random.choice(["buy", "sell"]),
            )
            trade.clean()
            trade.save()

        # Generate Futures
        for _ in range(50):
            trade = Trade(
                trade_date=self.create_random_date(),
                security_id=f"security_{random.randint(1000, 9999)}",
                username=random.choice(self.users).username,
                instrument_type="futures",
                strategy_id=f"strategy_{random.randint(100, 999)}",
                strategy="hedge",
                price=random.uniform(1, 500),
                direction=random.choice(["buy", "sell"]),
                no_of_contracts=random.uniform(1, 100),
            )
            trade.clean()
            trade.save()

        # Generate FX
        for _ in range(50):
            trade = Trade(
                trade_date=self.create_random_date(),
                security_id=f"security_{random.randint(1000, 9999)}",
                username=random.choice(self.users).username,
                instrument_type="fx",
                strategy_id=f"strategy_{random.randint(100, 999)}",
                strategy="hedge",
                price=random.uniform(1, 500),
                notional=random.randint(1, 100000000),
                direction=random.choice(["buy", "sell"]),
            )
            trade.clean()
            trade.save()

        self.stdout.write(
            self.style.SUCCESS("Successfully populated the database with Trades")
        )
