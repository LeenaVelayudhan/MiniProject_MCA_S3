# Generated by Django 5.1 on 2024-10-21 18:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_remove_besttimetovisit_destination_delete_attraction_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination_name', models.CharField(default='Unknown Destination', max_length=255)),
                ('href', models.CharField(default='/', max_length=255)),
                ('destination_description', models.TextField(blank=True, null=True)),
                ('country_name', models.CharField(default='Unknown Country', max_length=255)),
                ('country_description', models.TextField(blank=True, null=True)),
                ('continent_name', models.CharField(default='Unknown Continent', max_length=255)),
                ('continent_description', models.TextField(blank=True, null=True)),
                ('image_url', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BestTimeToVisit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('header_image', models.URLField(blank=True, null=True)),
                ('intropara', models.TextField(blank=True, null=True)),
                ('sections', models.JSONField(blank=True, null=True)),
                ('destination', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='best_time_to_visit', to='home.destination')),
            ],
        ),
        migrations.CreateModel(
            name='Attraction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attractions', to='home.destination')),
            ],
        ),
    ]