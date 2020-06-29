# Generated by Django 3.0.5 on 2020-06-29 12:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_app', '0016_auto_20200621_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipepost',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 29, 12, 38, 39, 969279, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='temporaryimage',
            name='image',
            field=models.ImageField(blank=True, upload_to='temporary'),
        ),
    ]