# Generated by Django 3.2.20 on 2023-07-10 09:11

from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Raw_Tweet',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False, unique=True)),
                ('id_tweet', models.IntegerField()),
                ('tweetText', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Analisis',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False, unique=True)),
                ('idioma', models.CharField(max_length=2)),
                ('rating', models.SmallIntegerField(default=0)),
                ('tipo', models.CharField(choices=[('E', 'Entrada'), ('T', 'Tweet')], default='E', max_length=1)),
                ('texto', models.TextField()),
                ('label', models.CharField(max_length=30)),
                ('score', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('label2', models.CharField(max_length=30)),
                ('score2', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('label3', models.CharField(max_length=30)),
                ('score3', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('raw_tweet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='analisis.raw_tweet')),
            ],
        ),
    ]
