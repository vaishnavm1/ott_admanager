# Generated by Django 4.0.5 on 2022-07-01 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_admin', '0033_order_discount_alloted_amt_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='discount_req_amt',
            field=models.IntegerField(default=0),
        ),
    ]
