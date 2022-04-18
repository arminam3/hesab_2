# Generated by Django 4.0.3 on 2022-04-09 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hesab', '0002_shopping_week'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopping',
            name='name',
            field=models.CharField(choices=[(0, 'شنبه'), (1, 'یکشنبه'), (2, 'دوشنبه'), (3, 'سه شنبه'), (4, 'چهارشنبه'), (5, 'پنج شنبه'), (6, 'جمعه')], default=1, max_length=100),
        ),
    ]
