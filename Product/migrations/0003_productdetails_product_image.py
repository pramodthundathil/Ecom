# Generated by Django 5.0.1 on 2024-02-20 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0002_productdetails_product_subcategory_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productdetails',
            name='Product_Image',
            field=models.FileField(null=True, upload_to='Produc_image'),
        ),
    ]