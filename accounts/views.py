from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView
from .forms import UserRegistrationForm, UserAddressForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordChangeDoneView
from .forms import CustomPasswordChangeForm
from django.shortcuts import render,redirect


User = get_user_model()


class UserRegistrationView(TemplateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/user_registration.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(
                reverse_lazy('transactions:transaction_report')
            )
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        registration_form = UserRegistrationForm(self.request.POST)
        address_form = UserAddressForm(self.request.POST)

        if registration_form.is_valid() and address_form.is_valid():
            user = registration_form.save()
            address = address_form.save(commit=False)
            address.user = user
            address.save()

            login(self.request, user)
            messages.success(
                self.request,
                (
                    f'Thank You For Creating A Bank Account. '
                    f'Your Account Number is {user.account.account_no}. '
                )
            )
            return HttpResponseRedirect(
                reverse_lazy('transactions:deposit_money')
            )

        return self.render_to_response(
            self.get_context_data(
                registration_form=registration_form,
                address_form=address_form
            )
        )

    def get_context_data(self, **kwargs):
        kwargs['registration_form'] = kwargs.get('registration_form', UserRegistrationForm())
        kwargs['address_form'] = kwargs.get('address_form', UserAddressForm())
        return super().get_context_data(**kwargs)

    

class UserLoginView(LoginView):
    template_name='accounts/user_login.html'
    redirect_authenticated_user = False


class LogoutView(RedirectView):
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().get_redirect_url(*args, **kwargs)
    
#password change 

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm  # Use your custom form class
    template_name = 'accounts/user_password_change.html'  # Specify the template for rendering the view

    def form_valid(self, form):
        # Log the user out from all sessions before changing the password
        logout(self.request)

        # Proceed with the password change
        super().form_valid(form)

        # Return a redirect response to a different URL
        return HttpResponseRedirect(reverse_lazy('accounts:password_change_done'))
    


class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'accounts/password_change_done_template.html'  # Specify the template for the password change done page
