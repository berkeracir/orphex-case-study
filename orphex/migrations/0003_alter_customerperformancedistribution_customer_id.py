# Generated by Django 5.1.1 on 2024-09-14 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orphex", "0002_performancedistribution_orphex_perf_fk_type_fccc1f_idx"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customerperformancedistribution",
            name="customer_id",
            field=models.TextField(),
        ),
    ]
