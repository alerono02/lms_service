# Generated by Django 4.2.7 on 2024-03-09 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_payment_stripe_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='date',
            field=models.DateField(auto_now_add=True, verbose_name='Дата оплаты'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='stripe_id',
            field=models.URLField(blank=True, max_length=255, null=True, verbose_name='ссылка для платежа'),
        ),
    ]