# Generated by Django 4.0.5 on 2022-07-27 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_admin', '0044_alter_order_bill_status_msg'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='client_type',
            field=models.CharField(default='Direct Client', max_length=252),
        ),
    ]
