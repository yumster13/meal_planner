# Generated by Django 4.2.11 on 2024-05-11 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0007_alter_recipexengredient_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='parent_tag',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='database.tag'),
        ),
    ]
