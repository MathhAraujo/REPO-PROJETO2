# Generated by Django 5.2 on 2025-04-16 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('studentId', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('studentName', models.CharField(max_length=100)),
                ('studentEmail', models.EmailField(max_length=254)),
                ('studentAge', models.PositiveIntegerField()),
            ],
        ),
    ]
