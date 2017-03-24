from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Balance


class BalanceTest(TestCase):

    def setUp(self):
        self.income = Balance.objects.create(
            amount=10000000,
            kind=Balance.INCOME,
            notes="thu nhap"
        )
        self.expense = Balance.objects.create(
            amount=5000000,
            kind=Balance.EXPENSE,
            notes="chi tieu"
        )

    def test_total_income_classmethod(self):
        self.assertEqual(Balance.total_income(), 10000000)

    def test_total_expense_classmethod(self):
        self.assertEqual(Balance.total_expense(), 5000000)

    def test_current_classmethod(self):
        self.assertEqual(Balance.current(), 5000000)


class BalanceViewTest(TestCase):
    TEST_USERNAME = 'test'
    TEST_PASSWORD = 'testpassword'

    def setUp(self):
        self.url = reverse('expenses:balance_list')
        self.income = Balance.objects.create(
            amount=10000000,
            kind=Balance.INCOME,
            notes="thu nhap"
        )
        self.expense = Balance.objects.create(
            amount=5000000,
            kind=Balance.EXPENSE,
            notes="chi tieu"
        )
        self.user = User.objects.create_user(
            username=self.TEST_USERNAME,
            password=self.TEST_PASSWORD
        )

    def test_i18n_view(self):
        self.client.login(username=self.TEST_USERNAME,
                          password=self.TEST_PASSWORD)
        response = self.client.get('/expenses/')
        self.assertRedirects(response, '/en/expenses/', target_status_code=302)
        response = self.client.get('/expenses/balance/')
        self.assertRedirects(response, self.url)

    def test_index_view(self):
        self.client.login(username=self.TEST_USERNAME,
                          password=self.TEST_PASSWORD)
        response = self.client.get('/en/expenses/')
        self.assertRedirects(response, self.url)

    def test_balance_view(self):
        self.client.login(username=self.TEST_USERNAME,
                          password=self.TEST_PASSWORD)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertSequenceEqual(
            response.context['object_list'],
            [
                self.income,
                self.expense,
            ]
        )
        self.assertEqual(response.context['current_balance'], 5000000)
