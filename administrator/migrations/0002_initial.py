# Generated by Django 4.1.3 on 2022-12-07 21:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administrator', '0001_initial'),
        ('booking', '0001_initial'),
        ('profile_user', '0002_alter_user_email'),
        ('inventory', '0002_itemcleaningroom_price_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='bookingspa',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='booking.bookingspa'),
        ),
        migrations.AddField(
            model_name='expenses',
            name='distributor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.distributor'),
        ),
        migrations.AddField(
            model_name='employeehistorybooking',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='profile_user.profileuser'),
        ),
    ]
