from django.shortcuts import render
from main.models import CombineVericle
from django.views.generic import ListView
from django.db.models import Sum, Count
from .resources import PersonResource
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from io import BytesIO
from datetime import datetime
import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.mail import send_mail, BadHeaderError
from django.views.decorators.csrf import csrf_exempt
from django.conf.global_settings import DEFAULT_FROM_EMAIL


class ListBorrower(ListView):
    model = CombineVericle
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(ListBorrower, self).get_context_data(**kwargs)
        context["verihcle_count"] = len(self.object_list)
        verihcle_states = CombineVericle.objects.values('account_status').annotate(Count("account_status"))
        # p = [{'account_status': 'O', 'account_status__count': 1}, {'account_status': 'P',
        #                                                                  'account_status__count': 1}, {
        #                'account_status': 'R', 'account_status__count': 1}]
        dict2 = {"O":"active", "R":"inactive", "P":"gps"}
        context["verihcle_states"] = dict([(dict2[state["account_status"]],state["account_status__count"]) for state in verihcle_states])
        return context

def export_csv(request):
    if request.method == "GET":
        person_resource = PersonResource()
        dataset = person_resource.export()
        response = HttpResponse(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="borrower.csv"'
        return response
    else:
        return render(request, template_name="index.html",
                      context={"message":"method not support", "status_code":405})

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def get_str(**kwargs):
    return_str = ""
    for key in kwargs:
        if kwargs[key] and not return_str:
            return_str = return_str + key
        else:
            return_str = return_str + " - " + key
    return return_str

def fetch_resources(uri, rel):
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    return path

def download_pdf(request, slug):
    if request.method == "GET":
        obj = get_object_or_404(CombineVericle, slug = slug)
        data = dict(cp_holder="Houston Direct Auto", cp_contact = "", cp_address = "4011 Jeanetta Street", cp_phone = "(832)252-1400",
                           cp_city_state = "Houston TX", cp_fax = "", cp_zip = "77063", cp_account = "6252551", cp_loan = "517241",
                           db_name = obj.borrower_full_name, db_address = obj.borrower_addredd, db_city_zip = get_str(borrower_city = obj.borrower_city,
                                                                                                                      borrower_zip_code = obj.borrower_zip_code),
                           db_phone = "", db_employer = "",
                           db_em_address = "", db_emp_city_zip = "", db_emp_phone = "", db_ssn = "", db_dl = "",
                           ds_name = "", ds_address = "", ds_city_zip = "", ds_phone = "", ds_employer = "",
                           ds_emp_address = "", ds_emp_city_zip = "", ds_bus_phone = "", ds_emp_phone = "",
                           stock = obj.collateral_stock_number, year = obj.collateral_year_model,
                           make = obj.collateral_make, model = obj.collateral_model, vin = obj.collateral_vin,
                           color = "", ignition = "",
                           license = "", gps_esn = "", payment_due_date = obj.actual_payment_past_due,
                           past_due_amount = obj.actual_payment_past_due,
                           late_charge_fee = 0, est_balance_owned = obj.account_total_balance,
                           days_past_due = obj.actual_days_past_due, contract_date = obj.contract_date,
                           signiture = obj.driver.signature, today_date = datetime.now())
        pdf = render_to_pdf('table.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
        # return render(request, template_name="table.html", context=data)
    else:
        return render(request, template_name="index.html",
                      context={"message": "method not support", "status_code": 405})

@csrf_exempt
def mail(request, slug):
    if request.method == "POST":
        obj = get_object_or_404(CombineVericle, slug = slug)
        comment = request.POST.get("comment")
        to_email = request.POST.get("email")
        subject = 'User Data'
        message = str(obj.__dict__) + "\n\n" + "Comment" + comment
        if subject and message:
            try:
                p = send_mail(subject, message, DEFAULT_FROM_EMAIL, [to_email],
                              fail_silently=False)
                print(p)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponse('Success')
        else:
            return HttpResponse('Falied')