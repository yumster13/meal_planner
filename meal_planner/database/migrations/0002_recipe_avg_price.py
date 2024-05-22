# Generated by Django 4.2.11 on 2024-05-11 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='avg_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Prix moyen'),
        ),
    ]