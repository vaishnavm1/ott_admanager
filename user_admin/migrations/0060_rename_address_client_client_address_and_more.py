# Generated by Django 4.0.5 on 2022-07-29 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_admin', '0059_rename_client_address_client_address_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='address',
            new_name='client_address',
        ),
        migrations.RenameField(
            model_name='client',
            old_name='company_name',
            new_name='client_company_name',
        ),
        migrations.RenameField(
            model_name='client',
            old_name='district',
            new_name='client_district',
        ),
        migrations.RenameField(
            model_name='client',
            old_name='email',
            new_name='client_email',
        ),
        migrations.RenameField(
            model_name='client',
            old_name='gst_number',
            new_name='client_gst_number',
        ),
        migrations.RenameField(
            model_name='client',
            old_name='mobile_no',
            new_name='client_mobile_no',
        ),
        migrations.RenameField(
            model_name='client',
            old_name='name',
            new_name='client_name',
        ),
        migrations.RenameField(
            model_name='client',
            old_name='taluka',
            new_name='client_taluka',
        ),
        migrations.RenameField(
            model_name='client',
            old_name='whatsapp_mobile_no',
            new_name='client_whatsapp_mobile_no',
        ),
    ]
