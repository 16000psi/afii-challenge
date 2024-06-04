# Generated by Django 5.0.6 on 2024-06-04 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trades', '0002_alter_potentialtrade_direction_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='potentialtrade',
            name='direction',
            field=models.CharField(blank=True, choices=[('buy', 'Buy'), ('sell', 'Sell')], max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='potentialtrade',
            name='no_of_contracts',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='potentialtrade',
            name='notional',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='potentialtrade',
            name='price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='potentialtrade',
            name='spread',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='trade',
            name='direction',
            field=models.CharField(blank=True, choices=[('buy', 'Buy'), ('sell', 'Sell')], max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='trade',
            name='no_of_contracts',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='trade',
            name='notional',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='trade',
            name='price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='trade',
            name='spread',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
