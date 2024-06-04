import logging
import os

import pandas as pd
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from trades.models import BondTrade, CDSTrade, FuturesTrade, FXTrade, Trade

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Populates the database with data from an XLSX file"

    def handle(self, *args, **kwargs):
        file_path = os.path.join(os.path.dirname(__file__), "../data/Data.xlsx")

        # Load the data from the XLSX file
        data = pd.read_excel(file_path)

        for index, row in data.iterrows():
            # Collect trade data
            trade_data = {
                "security_id": row["Security ID"],
                "username": row["User name"],
                "comment": row["Comment"],
                "strategy": row["Strategy"],
                "instrument_type": row["Instrument type"].lower(),
                "timestamp": row["timestamp"],
            }

            # Create the base Trade instance

            # Create an instance of the specific trade type
            try:
                if row["Instrument type"] == "Bonds":
                    BondTrade.objects.create(
                        **trade_data,
                        price=row["price"],
                        spread=row["Spread"],
                        notional=row["Notional"],
                        direction=row["Direction"],
                    )
                elif row["Instrument type"] == "CDS":
                    CDSTrade.objects.create(
                        **trade_data,
                        spread=row["Spread"],
                        notional=row["Notional"],
                        direction=row["Direction"],
                    )
                elif row["Instrument type"] == "Futures":
                    FuturesTrade.objects.create(
                        **trade_data,
                        price=row["price"],
                        no_of_contracts=row["Number of contracts"],
                        direction=row["Direction"],
                    )
                elif row["Instrument type"] == "FX":
                    FXTrade.objects.create(
                        **trade_data,
                        price=row["price"],
                        notional=row["Notional"],
                        direction=row["Direction"],
                    )
                logger.info(
                    f"Created specific Trade instance for row {index} ({row['Instrument type']})"
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Error creating specific trade instance at row {index}: {e}"
                    )
                )
                logger.error(
                    f"Error creating specific trade instance at row {index}: {e}"
                )

        self.stdout.write(self.style.SUCCESS("Database has been populated"))
