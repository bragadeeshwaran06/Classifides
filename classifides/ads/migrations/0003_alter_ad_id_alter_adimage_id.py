# Generated by Django 5.1 on 2024-08-21 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_alter_ad_id_alter_adimage_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='adimage',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
