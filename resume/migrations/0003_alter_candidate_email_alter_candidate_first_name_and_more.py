# Generated by Django 5.1.1 on 2024-09-11 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0002_rename_mobile_candidate_mobile_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='email',
            field=models.EmailField(max_length=255),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='first_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='mobile_number',
            field=models.CharField(max_length=200),
        ),
    ]
