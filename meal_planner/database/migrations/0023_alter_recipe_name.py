# Generated by Django 4.2.11 on 2024-05-27 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0022_ingredientxsu_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Nom'),
        ),
    ]