# Generated by Django 4.2 on 2023-06-23 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_category_products_description_products_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='title',
            field=models.TextField(max_length=100, null=True),
        ),
    ]
