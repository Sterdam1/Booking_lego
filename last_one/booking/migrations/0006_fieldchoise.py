# Generated by Django 5.0.4 on 2024-04-21 12:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_alter_newfield_created_by_bookinginfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='FieldChoise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choise', models.CharField(max_length=100)),
                ('field', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='booking.newfield')),
            ],
        ),
    ]
