# Generated by Django 4.2.11 on 2024-05-11 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0004_alter_ingredient_season'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='category',
        ),
    ]
