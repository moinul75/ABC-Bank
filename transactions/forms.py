import datetime
from typing import List
from django import forms
from . models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount' , 'transaction_type']
        
    def __init__(self , *args , **kwargs):
        self.account = kwargs.pop('account')
        super().__init__(*args , **kwargs)
        self.fields['transaction_type'].disabled =True
        self.fields['transaction_type'].widget = forms.HiddenInput
    def save(self , commit = True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()
    
class DepositeForm(TransactionForm):
    def clean_amount(self):
        min_deposite_amount = 100
        amount = self.cleaned_data.get('amount')
        
        if amount < min_deposite_amount:
            raise forms.ValidationError(f'You need to deposite at least {min_deposite_amount} $')
        return amount
    
class WithdrawForm(TransactionForm):
    def clean_data(self):
        account = self.account
        min_withdraw_amount = 100
        max_withdraw_amount = (account.account_type.maximum_withdrawal_amount)
        balance = account.balance
        amount = self.cleaned_data.get('account')
        
        if amount < min_withdraw_amount:
            raise forms.ValidationError(f'You can withdraw at least {min_withdraw_amount} $')
        if amount > max_withdraw_amount:
            raise forms.ValidationError(f'You can withdraw at most {max_withdraw_amount} $')
        if amount > balance:
            raise forms.ValidationError(f'You have {balance} $ in your account . You can not withdraw more than your account balance')
        return amount
    
class LoanRequestForm(TransactionForm):
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        return amount 
    
class TransferMoneyFormAccount(TransactionForm):
    receiver_account_no = forms.CharField(label="Receiver's Account No", max_length=100)
    def clean_receiver_account_no(self):
        # Get the receiver's account number from the cleaned data
        receiver_account_no = self.cleaned_data.get('receiver_account_no')
        # Add validation logic for the 'receiver_account_no' here if needed
        # For example, you can check if the account number exists in your database
        # or if it meets certain criteria.
        # You can raise a forms.ValidationError if validation fails.

        # Return the cleaned receiver account number
        return receiver_account_no
    def clean_amount(self):
        account_no = self.cleaned_data.get('account_no')
        min_transfer_amount = 100
        amount = self.cleaned_data.get('amount')
        account = self.account
        balance = account.balance
        
        if amount < min_transfer_amount:
            raise forms.ValidationError(f'You need to transfer at least {min_transfer_amount} $')
        #if this amount has his account or not 
        if amount > balance: 
            raise forms.ValidationError(f"You don't have enough money... you have only {balance} $")
        return amount
    def save(self , commit = True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()
    

