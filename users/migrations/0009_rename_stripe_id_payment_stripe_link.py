# Generated by Django 4.2.7 on 2024-03-09 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_payment_date_alter_payment_stripe_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='stripe_id',
            new_name='stripe_link',
        ),
    ]