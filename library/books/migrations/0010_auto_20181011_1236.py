# Generated by Django 2.1.1 on 2018-10-11 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0009_auto_20181010_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='late',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='rent',
            name='regulated_payment',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='rent',
            name='status',
            field=models.NullBooleanField(default=True),
        ),
    ]