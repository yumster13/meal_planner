# Generated by Django 4.2.11 on 2024-05-27 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0029_alter_recipe_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='category',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='database.category'),
        ),
    ]
