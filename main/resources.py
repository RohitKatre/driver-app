from import_export import resources
from .models import CombineVericle

class PersonResource(resources.ModelResource):
    class Meta:
        model = CombineVericle
        p = CombineVericle()
        fields = ['account_last_paid_date', 'borrower_full_name', 'account_total_balance', 'collateral_recovery_device',
                  'collateral_year_model', 'collateral_make', 'collateral_model', 'account_status', 'actual_days_past_due',
                  'collateral_stock_number', 'actual_payment_past_due', 'current_due_ammount', 'actual_record_flags',
                  'contract_date', 'last_event_date', 'longitude', 'latitue', 'primary_loan_cs_registration_payment_amt']