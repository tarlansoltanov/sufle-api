# Generated by Django 4.2.1 on 2023-06-03 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='logo',
            field=models.FileField(blank=True, null=True, upload_to='category/'),
        ),
    ]