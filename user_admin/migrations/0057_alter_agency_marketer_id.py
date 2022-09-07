# Generated by Django 4.0.5 on 2022-07-29 09:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_admin', '0056_agency_marketer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agency',
            name='marketer_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user_admin.marketer'),
        ),
    ]
