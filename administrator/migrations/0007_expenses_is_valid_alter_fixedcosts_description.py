# Generated by Django 4.1.3 on 2023-02-04 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0006_fixedcosts'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenses',
            name='is_valid',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='fixedcosts',
            name='description',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
