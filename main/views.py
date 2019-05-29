from django.shortcuts import render
from django.views.generic import FormView
from django.db import transaction
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model

from .forms import TransactionForm
from .models import Profile


User = get_user_model()

class MainFormView(SuccessMessageMixin, FormView):
    template_name = 'main.html'
    form_class = TransactionForm
    success_url = '/'

    # open a transaction
    @transaction.atomic
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        user_send_id         = self.request.POST['user_send_id']
        pay_user_profile    = User.objects.select_related('profile').get( id = user_send_id ).profile
        summ                = int(float(self.request.POST['summ'])*100)

        inn                 = self.request.POST['inn']
        users_recipients_id = Profile.objects.filter(inn = inn).exclude(user_id = user_send_id).values_list('id', flat=True)
        old_account         = pay_user_profile.account
        recipients_count    = users_recipients_id.count()
        pay_for_one_user    = summ//recipients_count

        pay_user_profile.account = old_account - pay_for_one_user * recipients_count
        pay_user_profile.save()
        recipient_profiles  = Profile.objects.filter(user_id__in = users_recipients_id)
        for p in recipient_profiles:
            old_account  = p.account
            p.account    = old_account + pay_for_one_user
            p.save()
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return 'Перевод прошел успешно!'