# Generated by Django 5.1 on 2024-09-03 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_alter_attraction_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attraction',
            name='category_image',
        ),
        migrations.AddField(
            model_name='attraction',
            name='category_headings',
            field=models.CharField(default='Default Category Heading', max_length=255),
        ),
        migrations.AlterField(
            model_name='attraction',
            name='category',
            field=models.CharField(choices=[('Harmony between Tradition and Modernity', 'Historical Places'), ('Gourmet Travel', 'Foods & Restaurants '), ('Nature and Its Healing Power', 'Nature'), ('Travel Activities', 'Activities'), ('Popular places (attractions)', 'Popular places'), ('Local Festivals', 'Local festivals')], max_length=50),
        ),
    ]
