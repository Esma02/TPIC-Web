# Generated by Django 4.0.3 on 2024-10-24 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hesaplama', '0002_mesaikaydi_delete_hesaplama'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mesaikaydi',
            name='aciklama',
            field=models.TextField(),
        ),
    ]
