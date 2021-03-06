# Generated by Django 3.2.5 on 2021-08-02 08:11

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('site', models.CharField(max_length=100)),
                ('when', models.CharField(max_length=150)),
                ('dateissued', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.CharField(max_length=200, unique=True)),
                ('nickname', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='EventParticipant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lucere_bot.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lucere_bot.user')),
            ],
        ),
    ]
