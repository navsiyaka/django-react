# Generated by Django 4.1.5 on 2023-12-18 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Datasource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Gaz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subsidiary', models.CharField(max_length=80, null=True, verbose_name='красный краб')),
                ('subsoil_user', models.CharField(max_length=80, null=True)),
                ('territory_type', models.CharField(max_length=80, null=True)),
                ('cost_item', models.CharField(max_length=80, null=True)),
                ('geographical_segments', models.CharField(max_length=80, null=True)),
                ('licensed_area', models.CharField(max_length=80, null=True)),
                ('data_type', models.CharField(max_length=80, null=True)),
                ('display', models.CharField(max_length=80, null=True)),
                ('value', models.IntegerField(null=True)),
            ],
            options={
                'unique_together': {('subsidiary', 'subsoil_user', 'territory_type', 'cost_item', 'geographical_segments', 'licensed_area', 'data_type', 'display', 'value')},
            },
        ),
        migrations.CreateModel(
            name='DayStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('clicks', models.IntegerField()),
                ('impressions', models.IntegerField()),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.campaign')),
                ('datasource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.datasource')),
            ],
            options={
                'ordering': ['date', 'datasource', 'campaign'],
                'unique_together': {('date', 'datasource', 'campaign')},
            },
        ),
    ]
