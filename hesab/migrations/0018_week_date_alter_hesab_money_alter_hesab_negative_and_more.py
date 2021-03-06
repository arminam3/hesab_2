# Generated by Django 4.0.3 on 2022-05-03 19:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hesab', '0017_hesab_money_hesab_negative_hesab_plus_hesab_week'),
    ]

    operations = [
        migrations.AddField(
            model_name='week',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='hesab',
            name='money',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='hesab',
            name='negative',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userhesab_n', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='hesab',
            name='plus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userhesab_p', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='hesab',
            name='week',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='weekhesab', to='hesab.week'),
        ),
        migrations.AlterField(
            model_name='shopping',
            name='consumer',
            field=models.ManyToManyField(default=(1, 2, 3, 4, 5, 6, 7, 8), to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='shopping',
            name='goods',
            field=models.CharField(default='غذا', max_length=500),
        ),
        migrations.AlterField(
            model_name='shopping',
            name='name',
            field=models.CharField(choices=[('0', 'شنبه'), ('1', 'یکشنبه'), ('2', 'دوشنبه'), ('3', 'سه شنبه'), ('4', 'چهارشنبه'), ('5', 'پنج شنبه'), ('6', 'جمعه')], default=0, max_length=100),
        ),
    ]
