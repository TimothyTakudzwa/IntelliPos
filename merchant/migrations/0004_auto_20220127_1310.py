# Generated by Django 3.2 on 2022-01-27 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchant', '0003_dummytransaction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='pos_terminal',
        ),
        migrations.DeleteModel(
            name='DummyTransaction',
        ),
        migrations.DeleteModel(
            name='Transaction',
        ),
    ]