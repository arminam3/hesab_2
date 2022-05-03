# Generated by Django 4.0.3 on 2022-05-03 04:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hesab', '0016_remove_hesab_money_remove_hesab_negative_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hesab',
            name='money',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='hesab',
            name='negative',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='userhesab_n', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='hesab',
            name='plus',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='userhesab_p', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='hesab',
            name='week',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='weekhesab', to='hesab.week'),
        ),
    ]