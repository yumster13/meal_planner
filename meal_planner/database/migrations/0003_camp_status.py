# Generated by Django 4.2.11 on 2024-05-11 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_recipe_avg_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='camp',
            name='status',
            field=models.CharField(choices=[('En Cours', 'C'), ('Fini', 'F')], default='En Cours', max_length=10, verbose_name='Status'),
        ),
    ]
