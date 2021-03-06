# Generated by Django 2.2 on 2019-04-16 07:31

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Borrower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('borrower_addredd', models.TextField(blank=True, null=True)),
                ('borrower_city', models.CharField(max_length=30)),
                ('borrower_state', models.CharField(max_length=10)),
                ('borrower_zip_code', models.IntegerField()),
                ('serial_number', models.CharField(max_length=20)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('phone_number', models.CharField(max_length=10)),
                ('signature', models.ImageField(upload_to='signature/16-04-2019-07-04')),
                ('repo_agent_id', models.CharField(max_length=20, unique=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Verhicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitue', models.DecimalField(decimal_places=6, max_digits=10)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=10)),
                ('last_out_for_repo_date', models.DateTimeField(blank=True, null=True)),
                ('collateral_recovery_device', models.CharField(max_length=20)),
                ('collateral_year_model', models.IntegerField(validators=[django.core.validators.MaxValueValidator(2019)])),
                ('collateral_make', models.CharField(max_length=24)),
                ('collateral_model', models.CharField(max_length=24)),
                ('collateral_stock_number', models.CharField(max_length=10)),
                ('collateral_vin', models.CharField(blank=True, max_length=32, null=True)),
                ('actual_record_flags', models.CharField(blank=True, max_length=120, null=True)),
                ('borrower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Borrower')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Driver')),
            ],
        ),
        migrations.CreateModel(
            name='BorrowerFinace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primary_loan_cs_registration_payment_amt', models.DecimalField(decimal_places=2, max_digits=10)),
                ('account_last_paid_data', models.DateTimeField(blank=True, null=True)),
                ('account_total_balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('account_status', models.CharField(choices=[('R', ''), ('P', ''), ('O', '')], max_length=2)),
                ('acctual_days_past_due', models.IntegerField(default=0)),
                ('actual_payment_past_due', models.DecimalField(decimal_places=2, max_digits=10)),
                ('current_due_ammount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('contract_data', models.DateTimeField(blank=True, null=True)),
                ('last_event_date', models.DateTimeField(auto_now=True)),
                ('borrower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Borrower')),
            ],
        ),
    ]
