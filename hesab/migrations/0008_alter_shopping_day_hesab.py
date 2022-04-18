# Generated by Django 4.0.3 on 2022-04-13 07:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hesab', '0007_alter_money_money'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopping',
            name='day',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.CreateModel(
            name='Hesab',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('negative', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userhesab_n', to=settings.AUTH_USER_MODEL)),
                ('plus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userhesab_p', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]