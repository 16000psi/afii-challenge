# Generated by Django 5.0.6 on 2024-06-04 00:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('trade_id', models.AutoField(primary_key=True, serialize=False)),
                ('security_id', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=30)),
                ('comment', models.CharField(blank=True, max_length=150)),
                ('strategy', models.CharField(max_length=50)),
                ('strategy_id', models.CharField(max_length=100)),
                ('instrument_type', models.CharField(choices=[('bond', 'Bond'), ('cds', 'CDS'), ('futures', 'Futures'), ('fx', 'FX')], editable=False, max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='BondTrade',
            fields=[
                ('trade_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='trades.trade')),
                ('price', models.FloatField()),
                ('spread', models.FloatField()),
                ('notional', models.FloatField()),
                ('direction', models.CharField(choices=[('buy', 'Buy'), ('sell', 'Sell')], max_length=4)),
            ],
            bases=('trades.trade',),
        ),
        migrations.CreateModel(
            name='CDSTrade',
            fields=[
                ('trade_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='trades.trade')),
                ('spread', models.FloatField()),
                ('notional', models.FloatField()),
                ('direction', models.CharField(choices=[('buy', 'Buy'), ('sell', 'Sell')], max_length=4)),
            ],
            bases=('trades.trade',),
        ),
        migrations.CreateModel(
            name='FuturesTrade',
            fields=[
                ('trade_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='trades.trade')),
                ('price', models.FloatField()),
                ('no_of_contracts', models.IntegerField()),
                ('direction', models.CharField(choices=[('buy', 'Buy'), ('sell', 'Sell')], max_length=4)),
            ],
            bases=('trades.trade',),
        ),
        migrations.CreateModel(
            name='FXTrade',
            fields=[
                ('trade_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='trades.trade')),
                ('price', models.FloatField()),
                ('notional', models.FloatField()),
                ('direction', models.CharField(choices=[('buy', 'Buy'), ('sell', 'Sell')], max_length=4)),
            ],
            bases=('trades.trade',),
        ),
    ]
