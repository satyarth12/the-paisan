# Generated by Django 3.0.7 on 2021-09-25 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Anouncement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='announcements/images/')),
                ('broadcast_on', models.DateTimeField()),
                ('sent', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-broadcast_on'],
            },
        ),
    ]
