# Generated by Django 2.2.8 on 2019-12-14 17:56

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LegalEntity',
            fields=[
                ('lei', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Bond',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isin', models.CharField(max_length=12)),
                ('size', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('currency', models.CharField(choices=[('GBP', 'British Pound'), ('EUR', 'Euro'), ('USD', 'US Dollar')], max_length=3)),
                ('maturity', models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(2019, 12, 14))])),
                ('lei', models.CharField(max_length=20)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('legal_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bonds.LegalEntity')),
            ],
        ),
    ]
