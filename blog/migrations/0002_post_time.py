# Generated by Django 5.0.1 on 2024-01-08 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='time',
            field=models.DateTimeField(auto_now_add=True, default='2024-01-01'),
            preserve_default=False,
        ),
    ]
