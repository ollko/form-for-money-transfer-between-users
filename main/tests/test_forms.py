from decimal import Decimal

from django.test import TestCase

from main.forms import TransactionForm
from main.tests.utils import set_user_data



class FormTests(TestCase):

    def setUp(self):
        super(FormTests, self).setUp()
        set_user_data()
        

    def test_valid_form(self):
        data = {'user_send_id': '1', 'summ': Decimal('10.00'), 'inn': 1234}
        form = TransactionForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.errors, {})

    def test_invalid_form_lack_of_users_with_this_inn(self):
        data = {'user_send_id': '1', 'summ': Decimal('10.00'), 'inn': 123}
        form = TransactionForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors,
            {'inn': ['Пользователей с указанным ИНН нет в базе данных.']}
        )

    def test_invalid_form_not_enough_funds_in_the_account_1(self):
        data = {'user_send_id': '1', 'summ': Decimal('121.00'), 'inn': 1234}
        form = TransactionForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors,
            {'user_send_id': ['На счете списания не достаточно средств.']}
        )

    def test_invalid_form_not_enough_funds_in_the_account_2(self):
        data = {'user_send_id': '1', 'summ': Decimal('0.01'), 'inn': 1234}
        form = TransactionForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors,
            {'user_send_id': ['На счете списания не достаточно средств.']}
        )

    def test_invalid_form_required_field_inn(self):
        data = {'user_send_id': '1', 'summ': Decimal('10.00')}
        form = TransactionForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'inn': ['Обязательное поле.']})

    def test_invalid_form_required_field_summ(self):
        data = {'user_send_id': '1', 'inn': 1234}
        form = TransactionForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'summ': ['Обязательное поле.']})

    def test_invalid_form_field_inn_required_field_summ_required(self):
        data = {'user_send_id': '1',}
        form = TransactionForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors,
            {'summ': ['Обязательное поле.'], 'inn': ['Обязательное поле.']})

    def test_invalid_form_not_enough_funds_in_the_account_lack_of_inn_field(self):
        data = {'user_send_id': '1', 'summ': Decimal('121.00')}
        form = TransactionForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors,
            {'user_send_id': ['На счете списания не достаточно средств.'],
            'inn': ['Обязательное поле.']}
        )

    def test_invalid_form_summ_field_can_not_null(self):
        data = {'user_send_id': '1', 'summ': Decimal('0.00'),'inn': 1234}
        form = TransactionForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'summ': ['Сумма перевода не должна быть равной нулю.']})

    def test_invalid_form_inn_field_can_not_null(self):
        data = {'user_send_id': '1', 'summ': Decimal('10.00'), 'inn': 0}
        form = TransactionForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'inn': ['ИНН не может быть равным нулю.']})

    def test_invalid_form_inn_field_can_not_null_inn_field_can_not_null(self):
        data = {'user_send_id': '1', 'summ': Decimal('0.00'), 'inn': 0}
        form = TransactionForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors,
            {'inn': ['ИНН не может быть равным нулю.'],
            'summ': ['Сумма перевода не должна быть равной нулю.']}
        )

    def test_invalid_form_(self):
        data = {'user_send_id': '6', 'summ': Decimal('20.00'), 'inn': 2222}
        form = TransactionForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors,
            {'inn': ['Это ИНН отправителя. Других пользователей с этим ИНН в базе нет.']}
        )
