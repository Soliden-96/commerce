# Generated by Django 4.2.4 on 2023-08-24 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_listing_imageurl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='currentBid',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
