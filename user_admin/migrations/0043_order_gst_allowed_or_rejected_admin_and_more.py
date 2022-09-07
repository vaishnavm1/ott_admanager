# Generated by Django 4.0.5 on 2022-07-21 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_admin', '0042_order_payment_accepted_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='gst_allowed_or_rejected_admin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gst_allowed_or_rejected_admin', to='user_admin.admin'),
        ),
        migrations.AddField(
            model_name='order',
            name='gst_relax_decision',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='gst_relax_requested',
            field=models.BooleanField(default=False),
        ),
    ]
