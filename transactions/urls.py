from django.urls import path
from . views import DepositeMoneyView , WithdrawMoneyView , TransactionReportView, LoanRequestView,LoanListView,PayLoanView,TranserMoneyFromOthers

app_name = 'transactions'

urlpatterns = [
    path("deposite/",DepositeMoneyView.as_view() , name= "deposit_money"),
    path("report/", TransactionReportView.as_view() , name = "transaction_report"),
    path("withdraw/" , WithdrawMoneyView.as_view() , name = "withdraw_money"),
    path("loan_request/" , LoanRequestView.as_view() , name = "loan_request"),
    path("loans/" , LoanListView.as_view() , name = "loan_list"),
    path("loans/<int:loan_id>/" , PayLoanView.as_view() , name = "pay"),
    path("transfer_money_from_another/",TranserMoneyFromOthers.as_view(),name='transfer_money_from_another'),
]
