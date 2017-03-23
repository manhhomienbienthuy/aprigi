from unittest import mock

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.timezone import datetime

from .models import Objective, Passbook, Withdraw


def faketoday():
    return datetime(2016, 6, 6)


class PassbookViewContextTest(TestCase):
    TEST_USERNAME = 'test'
    TEST_PASSWORD = 'testpassword'

    def setUp(self):
        self.today = datetime.today()
        self.url = reverse('savings:passbook_list')
        self.passbook = Passbook.objects.create(
            number="001",
            account_number="001",
            amount=10000000,
            period_type=2,
            period=1,
            rate=5.0,
            start_date=self.today,
            stop_date=self.today,
            is_open=True,
            notes="Note"
        )
        self.withdraw = Withdraw.objects.create(
            amount=10000000,
            date=self.today,
            is_open=True
        )
        self.objective = Objective.objects.create(
            year=self.today.year,
            amount=20000000
        )
        self.user = User.objects.create_user(
            username=self.TEST_USERNAME,
            password=self.TEST_PASSWORD
        )

    @mock.patch('django.utils.timezone.now', faketoday)
    def test_query_context(self):
        self.client.login(username=self.TEST_USERNAME,
                          password=self.TEST_PASSWORD)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['thisweek'], '2016-06-13')
        self.assertEqual(response.context['thismonth'], '2016-06-30')
        self.assertEqual(response.context['origin'], 10000000)
        self.assertEqual(response.context['interest'], 41667)

    def test_context_processsor_has_values(self):
        self.client.login(username=self.TEST_USERNAME,
                          password=self.TEST_PASSWORD)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['withdrawn'], 10000000)
        self.assertEqual(response.context['objective'], 20000000)
        self.assertEqual(response.context['current'], 10000000)
        self.assertEqual(response.context['percentage'], '50.00%')

    def test_context_processsor_all_closed(self):
        self.client.login(username=self.TEST_USERNAME,
                          password=self.TEST_PASSWORD)
        self.passbook.is_open = False
        self.passbook.save()
        self.withdraw.is_open = False
        self.withdraw.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['withdrawn'], 0)
        self.assertEqual(response.context['objective'], 20000000)
        self.assertEqual(response.context['current'], 0)
        self.assertEqual(response.context['percentage'], '0.00%')

    def test_context_processsor_all_empty(self):
        self.client.login(username=self.TEST_USERNAME,
                          password=self.TEST_PASSWORD)
        self.passbook.delete()
        self.withdraw.delete()
        self.objective.delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['withdrawn'], 0)
        self.assertEqual(response.context['objective'], 0)
        self.assertEqual(response.context['current'], 0)
        self.assertEqual(response.context['percentage'], '0.00%')
