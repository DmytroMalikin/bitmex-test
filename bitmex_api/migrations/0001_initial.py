# Generated by Django 3.0.7 on 2020-06-09 07:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('api_key', models.CharField(max_length=200)),
                ('api_secret', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Account',
                'verbose_name_plural': 'Accounts',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=200)),
                ('symbol', models.CharField(max_length=200)),
                ('volume', models.CharField(max_length=200)),
                ('side', models.BooleanField(blank=True, choices=[('Buy', False), ('Sell', True)], null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('price', models.FloatField()),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bitmex_api.Account')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
    ]