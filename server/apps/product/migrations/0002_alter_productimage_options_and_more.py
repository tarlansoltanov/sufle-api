# Generated by Django 4.2.1 on 2023-08-01 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productimage',
            options={'ordering': ['created_at'], 'verbose_name': 'ProductImage', 'verbose_name_plural': 'ProductImages'},
        ),
        migrations.AlterModelOptions(
            name='productweight',
            options={'ordering': ['person_count'], 'verbose_name': 'ProductWeight', 'verbose_name_plural': 'ProductWeights'},
        ),
    ]
