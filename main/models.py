from django.db import models
from django.contrib.auth.models import User
# Create your models here.
import datetime
import os, random
from django.template.defaultfilters import slugify
from django.utils.crypto import get_random_string
from django.core.validators import MaxValueValidator
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

ACCOUNT_STATUS = (
    ("R", "Recurrent"),
    ("P", "OpenRecurrent"),
    ("O", "TestRecurrent")
)

class Driver(User):
    phone_number = models.CharField(max_length=10, unique=False)
    signature = models.ImageField(upload_to=os.path.join("signature", datetime.datetime.now().strftime('%d-%m-%Y-%H-%m')))
    repo_agent_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True, unique=True)

    def __str__(self):
        string = self.first_name
        if self.last_name:
            string = string + " " + self.last_name
        string = string + " - " + self.email
        return string

    def save(self, *args, **kwargs):
        slug = slugify(self.first_name)
        try:
            qs_exists = Driver.objects.filter(slug=slug).exists()
            if qs_exists:
                slug = slug + "-" + get_random_string(4, str(random.randint(100000, 1000000)))
        except Exception as e:
            slug = slug + "-" + get_random_string(4, str(random.randint(100000, 1000000)))
        finally:
            self.slug = slug
            super(Driver, self).save(*args, **kwargs)

class Borrower(models.Model):
    name = models.CharField(max_length=50)
    borrower_addredd = models.TextField(null=True, blank=True)
    borrower_city = models.CharField(max_length=30)
    borrower_state = models.CharField(max_length=10)
    borrower_zip_code = models.IntegerField()
    serial_number = models.CharField(max_length=20)
    slug = models.SlugField(null=True, blank=True, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        try:
            qs_exists = Borrower.objects.filter(slug=slug).exists()
            if qs_exists:
                slug = slug + "-" + self.borrower_city + "-" + get_random_string(4, str(random.randint(100000, 1000000)))
        except Exception as e:
            slug = slug + "-" + self.borrower_city + "-" + get_random_string(4, str(random.randint(100000, 1000000)))
        finally:
            self.slug = slug
            super(Borrower, self).save(*args, **kwargs)

class BorrowerFinace(models.Model):
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    primary_loan_cs_registration_payment_amt = models.DecimalField(decimal_places=2, max_digits=10)
    account_last_paid_data = models.DateTimeField(null=True, blank=True)
    account_total_balance = models.DecimalField(decimal_places=2, max_digits=10)
    account_status = models.CharField(choices=ACCOUNT_STATUS, max_length=2)
    acctual_days_past_due = models.IntegerField(default=0)
    actual_payment_past_due = models.DecimalField(decimal_places=2, max_digits=10)
    current_due_ammount = models.DecimalField(decimal_places=2, max_digits=10)
    contract_data = models.DateTimeField(null=True, blank=True)
    last_event_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.borrower.name

class Verhicle(models.Model):
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    latitue = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    last_out_for_repo_date = models.DateTimeField(null=True, blank=True)
    collateral_recovery_device = models.CharField(max_length=20)
    collateral_year_model = models.IntegerField(validators=[MaxValueValidator(datetime.date.today().year)])
    collateral_make = models.CharField(max_length=24)
    collateral_model = models.CharField(max_length=24)
    collateral_stock_number = models.CharField(max_length=10)
    collateral_vin = models.CharField(max_length=32, null=True, blank=True)
    actual_record_flags = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return self.collateral_stock_number + " - " + self.borrower.name + " - " + str(self.driver.name)

class CombineVericle(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    borrower_full_name = models.CharField(max_length=50)
    borrower_addredd = models.CharField(max_length=255, null=True, blank=True)
    borrower_city = models.CharField(max_length=30, null=True, blank=True)
    borrower_state = models.CharField(max_length=10, null=True, blank=True)
    borrower_zip_code = models.IntegerField(null=True, blank=True)
    serial_number = models.CharField(max_length=20, null=True, blank=True)

    #finance
    primary_loan_cs_registration_payment_amt = models.DecimalField(decimal_places=2, max_digits=10)
    account_last_paid_date = models.DateTimeField(null=True, blank=True)
    account_total_balance = models.DecimalField(decimal_places=2, max_digits=10)
    account_status = models.CharField(choices=ACCOUNT_STATUS, max_length=2)
    actual_days_past_due = models.IntegerField(default=0)
    actual_payment_past_due = models.DecimalField(decimal_places=2, max_digits=10)
    current_due_ammount = models.DecimalField(decimal_places=2, max_digits=10)
    contract_date = models.DateTimeField(null=True, blank=True)
    last_event_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    #verhicle
    collateral_recovery_device = models.CharField(max_length=20)
    collateral_year_model = models.IntegerField(validators=[MaxValueValidator(datetime.date.today().year)])
    collateral_make = models.CharField(max_length=24)
    collateral_model = models.CharField(max_length=24)
    collateral_stock_number = models.CharField(max_length=10)
    collateral_vin = models.CharField(max_length=32, null=True, blank=True)
    latitue = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    last_out_for_repo_date = models.DateTimeField(null=True, blank=True)
    actual_record_flags = models.CharField(max_length=120, null=True, blank=True)

    slug = models.SlugField(null=True, blank=True, unique=True)

    def __str__(self):
        return self.borrower_full_name

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.borrower_full_name)
            try:
                qs_exists = CombineVericle.objects.filter(slug=slug).exists()
                if qs_exists and self.borrower_city:
                    slug = slug + "-" + self.borrower_city + "-" + get_random_string(4, str(random.randint(100000, 1000000)))
                else:
                    slug = slug + "-" + get_random_string(4, str(random.randint(100000, 1000000)))
            except Exception as e:
                slug = slug + "-" + get_random_string(4, str(random.randint(100000, 1000000)))
            finally:
                self.slug = slug
                super(CombineVericle, self).save(*args, **kwargs)
        else:
            super(CombineVericle, self).save(*args, **kwargs)
