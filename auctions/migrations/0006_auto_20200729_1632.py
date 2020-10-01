# Generated by Django 3.0.8 on 2020-07-29 10:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20200729_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bid_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_bids', to='auctions.Listing'),
        ),
        migrations.AlterField(
            model_name='bid',
            name='bid_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_bids', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_comments', to='auctions.Listing'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_uesr',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listing',
            name='list_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_lists', to=settings.AUTH_USER_MODEL),
        ),
    ]
