# Generated by Django 5.2 on 2025-06-05 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_profile_dados_calendario_json'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='coursesEval',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='student',
            name='coursesRegistred',
            field=models.TextField(blank=True, default=''),
        ),
    ]
