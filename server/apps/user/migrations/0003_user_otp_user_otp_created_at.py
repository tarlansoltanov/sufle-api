# Generated by Django 4.2.1 on 2023-06-17 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_birth_date_alter_user_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='otp',
            field=models.CharField(blank=True, max_length=6, null=True, verbose_name='otp'),
        ),
        migrations.AddField(
            model_name='user',
            name='otp_created_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='otp created at'),
        ),
    ]