# Generated by Django 3.2.20 on 2023-07-10 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analisis', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analisis',
            name='score',
            field=models.DecimalField(blank=True, decimal_places=15, max_digits=18, null=True),
        ),
        migrations.AlterField(
            model_name='analisis',
            name='score2',
            field=models.DecimalField(blank=True, decimal_places=15, max_digits=18, null=True),
        ),
        migrations.AlterField(
            model_name='analisis',
            name='score3',
            field=models.DecimalField(blank=True, decimal_places=15, max_digits=18, null=True),
        ),
    ]
