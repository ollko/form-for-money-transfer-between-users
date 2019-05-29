from decimal import Decimal

from django import forms
from django.contrib.auth import get_user_model

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from crispy_forms.layout import Field

from .models import Profile

User = get_user_model()


USER_CHOICES = User.objects.all().values_list('id','username')

class TransactionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout = Layout(
            Row(
                Column('user_send_id', css_class='form-group col-md-4 mb-0'),
                Column('summ', css_class='form-group col-md-4 mb-0'),
                Column('inn', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Перевести')
        )

    user_send_id = forms.ChoiceField(label = 'Счет списания', choices = USER_CHOICES)
    summ    = forms.DecimalField(label = 'Сумма', max_digits=10, decimal_places=2)
    inn     = forms.IntegerField(label = 'ИНН получателей')

    def clean(self):
        cleaned_data= super(TransactionForm, self).clean()
        user_send_id    = self.cleaned_data.get("user_send_id")
        summ            = self.cleaned_data.get("summ")
        inn             = self.cleaned_data.get("inn")
        # print('user_send_id', user_send_id)
        # print(User.objects.all().values_list('id', 'username'))
        u = User.objects.get( id = user_send_id )
        ac = u.profile.account
        if summ:
            summ  = int(summ*100)

        if (not summ) and (not inn):
            if summ == Decimal('0.00'):
                msg = "Сумма перевода не должна быть равной нулю."
                self.add_error('summ', msg)
            if inn == 0:
                msg = "ИНН не может быть равным нулю."
                self.add_error('inn', msg)
        elif not summ:
            if summ == Decimal('0.00'):
                msg = "Сумма перевода не должна быть равной нулю."
                self.add_error('summ', msg)
        elif not inn:
            if inn == 0:
                msg = "ИНН не может быть равным нулю."
                self.add_error('inn', msg)
            if ac//summ == 0:
                msg ="На счете списания не достаточно средств."
                self.add_error('user_send_id', msg)
        else:

            users_with_inn = User.objects.filter(profile__inn = inn)
            users_with_inn_count = User.objects.filter(profile__inn = inn).count()
            if not users_with_inn_count:
                msg = "Пользователей с указанным ИНН нет в базе данных."
                self.add_error('inn', msg)
            elif users_with_inn_count == 1 and users_with_inn.first().id is u.id:
                msg = 'Это ИНН отправителя. Других пользователей с этим ИНН в базе нет.'
                self.add_error('inn', msg)
            else:   
                if ac//summ == 0 or summ//users_with_inn_count == 0 :
                    msg ="На счете списания не достаточно средств."
                    self.add_error('user_send_id', msg)
