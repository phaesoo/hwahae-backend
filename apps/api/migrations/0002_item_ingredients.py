# Generated by Django 2.2.4 on 2020-01-08 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='ingredients',
            field=models.ManyToManyField(to='api.Ingredient'),
        ),
    ]
