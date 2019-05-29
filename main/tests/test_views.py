from decimal import Decimal

from django.urls import reverse
from django.test import TestCase

from main import views
from main.models import Profile
from main.tests.utils import set_user_data


class MainPageGetTests(TestCase):

    def setUp(self):
        super(MainPageGetTests, self).setUp()
        set_user_data()

    def test_main_page_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('main'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('main'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')

    def test_main_page_contains_correct_html(self):
        response = self.client.get('/')
        self.assertContains(response, '<h1 class="jumbotron-heading">Перевести указанную сумму</h1>')

    def test_main_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/')
        self.assertNotContains(
            response, 'Перевод прошел успешно!')

    def test_true_transaction(self):
        profiles =  Profile.objects.all()
        response = self.client.post('/', {'user_send_id': profiles[0].user.id, 'summ': Decimal('10.00'), 'inn': 1234})
        self.assertTrue(profiles[0].account == 11000 and profiles[1].account == 12500 and profiles[2].account == 500)

    def test_true_transaction_inn_sender_equal_inn_recipients(self):
        profiles =  Profile.objects.all()
        response = self.client.post('/', {'user_send_id': profiles[0].user.id, 'summ': Decimal('20.00'), 'inn': 1111})
        self.assertTrue(profiles[0].account == 10000 and profiles[1].account == 12000 \
                and profiles[2].account == 0 and profiles[3].account == 11000 and profiles[4].account == 21000)

    def test_true_transaction_summ_not_divided_by_the_number_of_recipients(self):
        profiles =  Profile.objects.all()
        response = self.client.post('/', {'user_send_id': profiles[0].user.id, 'summ': Decimal('20.01'), 'inn': 1111})
        # print('222 {} {} {} {} {}'.format(profiles[0].account,profiles[1].account,profiles[2].account,profiles[3].account,profiles[4].account))
        self.assertTrue(profiles[0].account == 10000 and profiles[1].account == 12000 \
                and profiles[2].account == 0 and profiles[3].account == 11000 and profiles[4].account == 21000)
