# Generated by Django 3.0.7 on 2021-09-25 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.IntegerField(blank=True, default=0, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='TV',
            fields=[
                ('id', models.IntegerField(blank=True, default=0, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=300)),
            ],
        ),
    ]