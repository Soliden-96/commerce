# Generated by Django 4.2.4 on 2023-08-25 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_listing_currentbid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='startingBid',
            new_name='startingPrice',
        ),
    ]