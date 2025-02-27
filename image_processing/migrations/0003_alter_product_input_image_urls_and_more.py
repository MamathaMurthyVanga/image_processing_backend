# Generated by Django 5.1.6 on 2025-02-25 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_processing', '0002_alter_product_input_image_urls_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='input_image_urls',
            field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='output_image_urls',
            field=models.JSONField(default=list),
        ),
    ]
