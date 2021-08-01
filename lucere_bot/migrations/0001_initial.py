# Generated by Django 3.2.5 on 2021-08-01 09:16

from django.db import migrations, models


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
                ('dateissued', models.DateTimeField()),
            ],
        ),
    ]
