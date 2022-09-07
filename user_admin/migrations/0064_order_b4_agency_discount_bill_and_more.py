# Generated by Django 4.0.5 on 2022-07-30 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_admin', '0063_order_agency_discount_amt_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='b4_agency_discount_bill',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='mode_of_pay',
            field=models.CharField(choices=[('Cash', 'Cash'), ('Upi', 'Upi'), ('Cheque', 'Cheque'), ('Net-Banking', 'Net Banking'), ('Pdc_Cheque', 'Pdc Cheque'), ('None', 'None')], default='None', max_length=100),
        ),
    ]
