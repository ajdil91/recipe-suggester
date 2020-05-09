# Generated by Django 3.0.5 on 2020-05-09 06:15

import ckeditor.fields
import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_app', '0011_auto_20200509_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipepost',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 9, 6, 15, 44, 474569, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='recipepost',
            name='ingredients',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
