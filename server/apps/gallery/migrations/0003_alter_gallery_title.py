# Generated by Django 4.2.1 on 2023-07-18 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_gallery_url_alter_gallery_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
