# Generated by Django 4.0.4 on 2022-05-23 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_buyproduct_oderd_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buyproduct',
            name='cart',
        ),
        migrations.AddField(
            model_name='buyproduct',
            name='cart',
            field=models.ManyToManyField(to='myapp.mycart'),
        ),
    ]
