# Generated by Django 4.2.1 on 2023-07-20 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('type', models.PositiveSmallIntegerField(choices=[(0, 'Şikayət'), (1, 'Təklif'), (2, 'Vakansiya')], default=1)),
                ('message', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
                'ordering': ['-modified_at'],
                'abstract': False,
            },
        ),
    ]
