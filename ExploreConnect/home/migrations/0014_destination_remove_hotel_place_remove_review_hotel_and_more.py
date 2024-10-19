# Generated by Django 5.1 on 2024-10-16 05:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_hotel_image_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination_name', models.CharField(max_length=255)),
                ('country_name', models.CharField(max_length=255)),
                ('continent_name', models.CharField(max_length=255)),
                ('continent_description', models.TextField()),
                ('destination_description', models.TextField()),
                ('image_url', models.URLField()),
                ('weather_data', models.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='place',
        ),
        migrations.RemoveField(
            model_name='review',
            name='hotel',
        ),
        migrations.CreateModel(
            name='Attraction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Historical Places', 'Harmony between Tradition and Modernity'), ('Foods & Restaurants ', 'Gourmet Travel'), ('Nature', 'Nature and Its Healing Power'), ('Activities', 'Travel Activities'), ('Popular places', 'Popular places (attractions)'), ('Local festivals', 'Local Festivals')], max_length=50)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='attractions/')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attractions', to='home.destination')),
            ],
        ),
        migrations.DeleteModel(
            name='Place',
        ),
        migrations.DeleteModel(
            name='Hotel',
        ),
        migrations.DeleteModel(
            name='Review',
        ),
    ]
