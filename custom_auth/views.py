from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import CreateView

from custom_auth.forms import *

# Create your views here.
from custom_auth.tokens import account_activation_token


class RegistrationView(CreateView):
    model = User
    # template_name = ''
    form_class = UserForm
    # success_url = '/custom/login'
    template_name = 'register.html'

    def form_valid(self, form):
        form.save()
        return redirect('custom_auth:login')

    # def post(self, request, *args, **kwargs):
    #     if request.method == 'POST':
    #         form = UserForm(request.POST)
    #         if form.is_valid():
    #             user = form.save(commit=False)
    #             user.is_active = False
    #             user.save()
    #             current_site = get_current_site(request)
    #             subject = 'Activate Your MySite Account'
    #             message = render_to_string('account_activation.html', {
    #                 'user': user,
    #                 'domain': current_site.domain,
    #                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
    #                 'token': account_activation_token.make_token(user),
    #             })
    #             user.email_user(subject, message)
    #             return redirect('account_activation_sent')
    #     else:
    #         form = UserForm()
    #     return render(request, 'register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        user = self.request.user

        if user.role == 'company':
            return reverse('company:company_dashboard_index')

        else:
            return reverse('job_seeker:seeker_dashboard_index')


class CustomLogoutView(LogoutView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return redirect('custom_auth:login')


class UserPasswordResetView(PasswordResetView):
    template_name = 'password_reset_form.html'
    success_url = reverse_lazy('custom_auth:password_reset_done')
    subject_template_name = 'password_reset_subject.txt'
    email_template_name = 'password_reset_email.html'


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('home:index')
    form_valid_message = "Your password was changed!"


# class AccountActivationView(View):
#     def activate(request, uidb64, token):
#         try:
#             uid = force_text(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#             user = None
#
#         if user is not None and account_activation_token.check_token(user, token):
#             user.is_active = True
#             user.profile.email_confirmed = True
#             user.save()
#             login(request, user)
#             return redirect('home')
#         else:
#             return render(request, 'account_activation_invalid.html')
