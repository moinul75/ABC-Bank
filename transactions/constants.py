DEPOSIT = 1
WITHDRAWAL = 2
LOAN = 3
LOAN_PAID = 4
TRANSFER_FORM_OTHER = 5

TRANSACTION_TYPE_CHOICES = (
    (DEPOSIT , 'Deposit'),
    (WITHDRAWAL , 'Withdrawal'),
    (LOAN , 'Loan'),
    (LOAN_PAID , 'Loan_paid'),
    (TRANSFER_FORM_OTHER, 'Transfer_from_other')
)