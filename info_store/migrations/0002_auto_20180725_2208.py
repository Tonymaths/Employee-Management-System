# Generated by Django 2.0.7 on 2018-07-25 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info_store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='number',
            field=models.DecimalField(decimal_places=0, max_digits=12),
        ),
    ]