# Generated by Django 4.0.4 on 2022-05-23 10:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_remove_buyproduct_cart_buyproduct_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyproduct',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
