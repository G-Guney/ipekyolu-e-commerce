# Generated by Django 4.2 on 2023-06-23 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_alter_products_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.category'),
        ),
    ]