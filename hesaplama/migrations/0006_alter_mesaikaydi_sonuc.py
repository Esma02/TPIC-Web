# Generated by Django 4.0.3 on 2024-11-05 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hesaplama', '0005_alter_mesaikaydi_aciklama_alter_mesaikaydi_kule_adi_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mesaikaydi',
            name='sonuc',
            field=models.CharField(max_length=5),
        ),
    ]
