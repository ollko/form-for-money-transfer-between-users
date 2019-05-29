from django.test import TestCase
from django.contrib.auth import get_user_model

from main.models import Profile

User = get_user_model()

def set_user_data():
    u1 = User.objects.create(username='Vania',email='vania@yandex.ru', password = '1234')
    u1.profile.inn = 1111
    u1.profile.account = 12000
    u1.save()

    u2 = User.objects.create(username='Foo',email='foo@yandex.ru', password = '1234')
    u2.profile.inn = 1234
    u2.profile.account = 12000
    u2.save()

    u3 = User.objects.create(username='Buzz',email='buzz@yandex.ru', password = '1234')
    u3.profile.inn = 1234
    u3.profile.account = 0
    u3.save()

    u4 = User.objects.create(username='Olga',email='olga@yandex.ru', password = '1234')
    u4.profile.inn = 1111
    u4.profile.account = 10000
    u4.save()

    u5 = User.objects.create(username='Fedor',email='fedor@yandex.ru', password = '1234')
    u5.profile.inn = 1111
    u5.profile.account = 20000
    u5.save()

    u6 = User.objects.create(username='Vera',email='Vera@yandex.ru', password = '1234')
    u6.profile.inn = 2222
    u6.profile.account = 30000
    u6.save()
