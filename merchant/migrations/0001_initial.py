# Generated by Django 3.1.7 on 2021-03-18 09:15

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('pass_hash', models.BinaryField()),
                ('otp', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(default='263', max_length=20)),
                ('role', models.CharField(choices=[('ADMIN', 'ADMIN'), ('TELLER', 'TELLER')], default='', max_length=20)),
                ('pin_tries', models.IntegerField(default=3)),
                ('locked', models.BooleanField(default=False)),
                ('password_change', models.DateField(default=datetime.datetime(2021, 6, 16, 11, 15, 24, 246387))),
                ('unlocks_at', models.DateTimeField(default=datetime.datetime(2021, 3, 18, 11, 45, 24, 246387))),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(max_length=30)),
                ('balance', models.FloatField(blank=True, default=0)),
                ('destination_bank', models.CharField(choices=[('AFC', 'AFC'), ('AGRIBANK', 'AGRIBANK'), ('BANC ABC', 'BANC ABC'), ('CABS', 'CABS'), ('CBZ', 'CBZ'), ('ECOBANK', 'ECOBANK'), ('FBC', 'FBC'), ('FBC BS', 'FBC BS'), ('FIRST CAPITAL BANK', 'FIRST CAPITAL BANK'), ('GETBUCKS', 'GETBUCKS'), ('NEDBANK', 'NEDBANK'), ('METBANK', 'METBANK'), ('MFS', 'MFS'), ('NBS', 'NBS'), ('NMB', 'NMB'), ('POSB', 'POSB'), ('STANBIC BANK', 'STANBIC BANK'), ('STANDARD CHARTERED', 'STANDARD CHARTERED'), ('STEWARD BANK', 'STEWARD BANK'), ('ONEMONEY', 'ONEMONEY'), ('EMPOWER BANK', 'EMPOWER BANK'), ('ZB BANK', 'ZB BANK')], default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='IntelliPos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pos_id', models.CharField(default='', max_length=20)),
                ('last_logged_device', models.CharField(max_length=255)),
                ('last_active_time', models.CharField(max_length=255)),
                ('is_logged_in', models.BooleanField(default=False)),
                ('active_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100, unique=True)),
                ('address', models.CharField(default='', max_length=255)),
                ('email', models.CharField(default='', max_length=50)),
                ('phone_number', models.CharField(default='', max_length=30)),
                ('industry', models.CharField(choices=[('Accounting', 'Accounting'), ('Airlines / Aviation', 'Airlines / Aviation'), ('Alternative Dispute Resolution', 'Alternative Dispute Resolution'), ('Alternative Medicine', 'Alternative Medicine'), ('Animation', 'Animation'), ('Apparel / Fashion', 'Apparel / Fashion'), ('Architecture / Planning', 'Architecture / Planning'), ('Arts / Crafts', 'Arts / Crafts'), ('Automotive', 'Automotive'), ('Aviation / Aerospace', 'Aviation / Aerospace'), ('Banking / Mortgage', 'Banking / Mortgage'), ('Biotechnology / Greentech', 'Biotechnology / Greentech'), ('Broadcast Media', 'Broadcast Media'), ('Building Materials', 'Building Materials'), ('Business Supplies / Equipment', 'Business Supplies / Equipment'), ('Capital Markets / Hedge Fund / Private Equity', 'Capital Markets / Hedge Fund / Private Equity'), ('Chemicals', 'Chemicals'), ('Civic / Social Organization', 'Civic / Social Organization'), ('Civil Engineering', 'Civil Engineering'), ('Commercial Real Estate', 'Commercial Real Estate'), ('Computer Games', 'Computer Games'), ('Computer Hardware', 'Computer Hardware'), ('Computer Networking', 'Computer Networking'), ('Computer Software / Engineering', 'Computer Software / Engineering'), ('Computer / Network Security', 'Computer / Network Security'), ('Construction', 'Construction'), ('Consumer Electronics', 'Consumer Electronics'), ('Consumer Goods', 'Consumer Goods'), ('Consumer Services', 'Consumer Services'), ('Cosmetics', 'Cosmetics'), ('Dairy', 'Dairy'), ('Defense / Space', 'Defense / Space'), ('Design', 'Design'), ('E - Learning', 'E - Learning'), ('Education Management', 'Education Management'), ('Electrical / Electronic Manufacturing', 'Electrical / Electronic Manufacturing'), ('Entertainment / Movie Production', 'Entertainment / Movie Production'), ('Environmental Services', 'Environmental Services'), ('Events Services', 'Events Services'), ('Executive Office', 'Executive Office'), ('Facilities Services', 'Facilities Services'), ('Farming', 'Farming'), ('Financial Services', 'Financial Services'), ('Fine Art', 'Fine Art'), ('Fishery', 'Fishery'), ('Food Production', 'Food Production'), ('Food / Beverages', 'Food / Beverages'), ('Fundraising', 'Fundraising'), ('Furniture', 'Furniture'), ('Gambling / Casinos', 'Gambling / Casinos'), ('Glass / Ceramics / Concrete', 'Glass / Ceramics / Concrete'), ('Government Administration', 'Government Administration'), ('Government Relations', 'Government Relations'), ('Graphic Design / Web Design', 'Graphic Design / Web Design'), ('Health / Fitness', 'Health / Fitness'), ('Higher Education / Acadamia', 'Higher Education / Acadamia'), ('Hospital / Health Care', 'Hospital / Health Care'), ('Hospitality', 'Hospitality'), ('Human Resources / HR', 'Human Resources / HR'), ('Import / Export', 'Import / Export'), ('Individual / Family Services', 'Individual / Family Services'), ('Industrial Automation', 'Industrial Automation'), ('Information Services', 'Information Services'), ('Information Technology / IT', 'Information Technology / IT'), ('Insurance', 'Insurance'), ('International Affairs', 'International Affairs'), ('International Trade / Development', 'International Trade / Development'), ('Internet', 'Internet'), ('Investment Banking / Venture', 'Investment Banking / Venture'), ('Investment Management / Hedge Fund / Private Equity', 'Investment Management / Hedge Fund / Private Equity'), ('Judiciary', 'Judiciary'), ('Law Enforcement', 'Law Enforcement'), ('Law Practice / Law Firms', 'Law Practice / Law Firms'), ('Legal Services', 'Legal Services'), ('Legislative Office', 'Legislative Office'), ('Leisure / Travel', 'Leisure / Travel'), ('Library', 'Library'), ('Logistics / Procurement', 'Logistics / Procurement'), ('Luxury Goods / Jewelry', 'Luxury Goods / Jewelry'), ('Machinery', 'Machinery'), ('Market Research', 'Market Research'), ('Marketing / Advertising / Sales', 'Marketing / Advertising / Sales'), ('Mechanical or Industrial Engineering', 'Mechanical or Industrial Engineering'), ('Media Production', 'Media Production'), ('Medical ', 'Medical '), ('Military Industry', 'Military Industry'), ('Mining / Metals', 'Mining / Metals'), ('Music', 'Music'), ('Newspapers / Journalism', 'Newspapers / Journalism'), ('Non - Profit / Volunteering', 'Non - Profit / Volunteering'), ('Oil / Energy / Solar / Greentech', 'Oil / Energy / Solar / Greentech'), ('Other Industry', 'Other Industry'), ('Pharmaceuticals', 'Pharmaceuticals'), ('Political Organization', 'Political Organization'), ('Primary / Secondary Education', 'Primary / Secondary Education'), ('Printing', 'Printing'), ('Real Estate / Mortgage', 'Real Estate / Mortgage'), ('Restaurants', 'Restaurants'), ('Retail Industry', 'Retail Industry'), ('Sports', 'Sports'), ('Telecommunications', 'Telecommunications'), ('Transportation', 'Transportation')], default='', max_length=100)),
                ('company_type', models.CharField(choices=[('SOLE TRADER', 'SOLE TRADER'), ('PRIVATE LIMITED COMPANY', 'Private Limited Company'), ('PRIVATE BUSINESS Corporate', 'Private Business Corporate')], default='', max_length=30)),
                ('account', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='merchant_account', to='merchant.account')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('sender_account', models.CharField(blank=True, default='', max_length=30)),
                ('receiver_account', models.CharField(blank=True, default='', max_length=30)),
                ('destination_bank', models.CharField(blank=True, default='', max_length=50)),
                ('amount', models.FloatField(blank=True, default=0.0)),
                ('currency', models.CharField(blank=True, default='USD', max_length=255)),
                ('reference', models.CharField(blank=True, default='', max_length=255)),
                ('status', models.BooleanField(default=False)),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='merchant.merchant')),
                ('pos', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='writer_merchant', to='merchant.intellipos')),
            ],
        ),
        migrations.CreateModel(
            name='PasswordHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password_hash_1', models.TextField(blank=True, null=True)),
                ('password_hash_2', models.TextField(blank=True, null=True)),
                ('password_hash_3', models.TextField(blank=True, null=True)),
                ('password_hash_4', models.TextField(blank=True, null=True)),
                ('next_cycle', models.IntegerField(default=1)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='intellipos',
            name='merchant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='merchant.merchant'),
        ),
        migrations.AddField(
            model_name='user',
            name='merchant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='merchant.merchant'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
