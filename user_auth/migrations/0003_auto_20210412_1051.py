# Generated by Django 3.1.7 on 2021-04-12 10:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0002_user_is_merchant_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='logon_attempts',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='PasswordHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password_hash', models.BinaryField()),
                ('date_created', models.DateField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]