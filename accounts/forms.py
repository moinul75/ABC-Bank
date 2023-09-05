from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.db import transaction
from . models import User , UserBankAccount , UserAddress , BankAccountType
from . constant import GENDER_CHOICE

class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = [
            'street_address',
            'city',
            'postal_code',
            'country',
        ]
    def __init__(self, *args , **kwargs):
        super().__init__(*args , **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })
            
class UserRegistrationForm(UserCreationForm):
    account_type = forms.ModelChoiceField(queryset= BankAccountType.objects.all())
    gender = forms.ChoiceField(choices=GENDER_CHOICE)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    first_name = forms.CharField(max_length=20 , widget=forms.TextInput(attrs={'autofocus':'on'}))
    last_name = forms.CharField(max_length=20)
    email = forms.CharField(max_length=20 , widget=forms.EmailInput(attrs={'autofocus':'off'}))
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            "class": "text-sm text-gray-500 mr-5 py-2 px-6 rounded-full border-0 text-sm font-medium bg-blue-50 text-blue-700 hover:cursor-pointer hover:bg-amber-50 hover:text-amber-700",
            "type": "file"
        })
    )
    
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'profile_picture'
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })

    @transaction.atomic
    def save(self , commit = True):
        user = super().save(commit=False)
        user.set_password = self.cleaned_data['password1']
        if commit:
            user.save()
            account_type = self.cleaned_data.get('account_type')
            gender = self.cleaned_data.get('gender')
            birth_date = self.cleaned_data.get('birth_date')
            UserBankAccount.objects.create(
                user = user ,
                gender = gender,
                brith_date = birth_date,
                account_type = account_type,
                account_no = (
                    user.id+
                    settings.ACCOUNT_NUMBER_START_FROM
                )
            )
        return user
    
    
#change password forms 
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput(attrs={
            "class": "your-custom-class-here",
        })
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={
            "class": "your-custom-class-here",
        })
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={
            "class": "your-custom-class-here",
        })
    )
