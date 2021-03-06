# Generated by Django 3.2.5 on 2021-07-02 00:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210701_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.customer'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.seller'),
        ),
    ]
