from django.urls import path
from .views import *

urlpatterns = [
    path('', ListBorrower.as_view(), name="list"),
    path('export/', export_csv, name="export"),
    path('download_invoice/<slug:slug>/', download_pdf, name="export_invoice"),
    path('mail/<slug:slug>/', mail, name="mail"),
]
