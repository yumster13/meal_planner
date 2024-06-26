# Generated by Django 4.2.11 on 2024-05-11 08:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('road', models.CharField(max_length=30, verbose_name='Rue')),
                ('town', models.CharField(max_length=30, verbose_name='Ville')),
                ('number', models.CharField(max_length=30, verbose_name='Numéro')),
                ('codePostal', models.CharField(max_length=4, verbose_name='CodePostal')),
                ('country', models.CharField(max_length=4, verbose_name='Pays')),
            ],
        ),
        migrations.CreateModel(
            name='Camp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Nom')),
                ('from_date', models.DateField(blank=True, null=True, verbose_name='De')),
                ('to_date', models.DateField(blank=True, null=True, verbose_name='A')),
                ('deadline', models.DateField(default='2024-01-01', verbose_name='Deadline')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='database.address')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Nom')),
                ('parent_category', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='database.category')),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Nom')),
                ('season', models.CharField(choices=[('18+', 'Default'), ('6-8', 'Baladins'), ('8-12', 'Louveteaux'), ('12-16', 'Troupe'), ('16-18', 'Pios')], default='18+', max_length=10, verbose_name='Saison')),
                ('mesurement', models.CharField(choices=[('KG', 'Kg'), ('L', 'L'), ('PIECES', 'Pieces')], default='KG', max_length=10, verbose_name='Mesure')),
                ('avg_price', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Prix moyen')),
                ('category', models.ManyToManyField(to='database.category')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Nom')),
                ('age', models.CharField(choices=[('18+', 'Default'), ('6-8', 'Baladins'), ('8-12', 'Louveteaux'), ('12-16', 'Troupe'), ('16-18', 'Pios')], default='18+', max_length=10, verbose_name="Tranche d'âge")),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Nom')),
                ('parent_tag', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='database.tag')),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Quantité')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='database.ingredient')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeXEngridient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Quantité')),
                ('age', models.CharField(choices=[('18+', 'Default'), ('6-8', 'Baladins'), ('8-12', 'Louveteaux'), ('12-16', 'Troupe'), ('16-18', 'Pios')], default='18+', max_length=10, verbose_name="Tranche d'âge")),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='database.ingredient')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Nom')),
                ('prairie', models.BooleanField(default=False, verbose_name='En prairie ?')),
                ('ingredients', models.ManyToManyField(to='database.recipexengridient')),
                ('tags', models.ManyToManyField(to='database.tag')),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nbr_anim', models.IntegerField(verbose_name="nombre d'animés")),
                ('nbr_leaders', models.IntegerField(verbose_name="nombre d'animateurs")),
                ('nbr_vege', models.IntegerField(verbose_name='nombre de vegetariens')),
                ('date', models.DateField(verbose_name='Jour')),
                ('moment', models.CharField(choices=[('MATIN', 'Matin'), ('MIDI', 'Midi'), ('GOUTER', 'Gouter'), ('SOUPER', 'Souper'), ('5EME', 'Cinqieme')], default='MATIN', max_length=10, verbose_name='Moment de la journée')),
                ('camp', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='database.camp')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='database.recipe')),
            ],
        ),
        migrations.AddField(
            model_name='camp',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='database.section'),
        ),
    ]
