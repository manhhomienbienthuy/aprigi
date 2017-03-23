from calendar import monthrange
from datetime import datetime, timedelta

from django.contrib.auth.models import Permission, User
from django.core.urlresolvers import reverse
from django.test import TestCase

from .forms import PassbookSearchForm, PassbookWithdrawForm
from .models import Passbook, Withdraw


class PassbookViewTest(TestCase):
    TEST_USERNAME = 'test'
    TEST_PASSWORD = 'testpassword'

    def setUp(self):
        self.today = datetime.today()
        self.url = reverse('savings:passbook_list')
        self.closed_passbook = Passbook.objects.create(
            number="001",
            account_number="001",
            amount=10000000,
            period_type=2,
            period=1,
            rate=5.0,
            start_date=self.today,
            stop_date=self.today,
            is_open=False,
            notes="Note"
        )
        self.today_passbook = Passbook.objects.create(
            number="002",
            account_number="002",
            amount=10000000,
            period_type=2,
            period=1,
            rate=5.0,
            start_date=self.today,
            stop_date=self.today,
            is_open=True,
            notes="Note"
        )
        self.this_week_passbook = Passbook.objects.create(
            number="003",
            account_number="003",
            amount=10000000,
            period_type=2,
            period=1,
            rate=5.0,
            start_date=self.today,
            stop_date=self.today + timedelta(days=1),
            is_open=True,
            notes="Note"
        )
        self.this_month_passbook = Passbook.objects.create(
            number="004",
            account_number="004",
            amount=10000000,
            period_type=2,
            period=1,
            rate=5.0,
            start_date=self.today,
            stop_date=datetime(self.today.year, self.today.month,
                               monthrange(self.today.year, self.today.month)[1]
                               ).date(),
            is_open=True,
            notes="Note"
        )
        self.next_month_passbook = Passbook.objects.create(
            number="005",
            account_number="005",
            amount=10000000,
            period_type=2,
            period=1,
            rate=5.0,
            start_date=self.today,
            stop_date=self.today + timedelta(days=31),
            is_open=True,
            notes="Note"
        )
        self.next_year_passbook = Passbook.objects.create(
            number="006",
            account_number="006",
            amount=10000000,
            period_type=2,
            period=1,
            rate=5.0,
            start_date=self.today,
            stop_date=self.today + timedelta(days=367),
            is_open=True,
            notes="Note"
        )
        Withdraw.objects.create(
            amount=10000000,
            date=self.today,
            is_open=True
        )
        self.user = User.objects.create_user(
            username=self.TEST_USERNAME,
            password=self.TEST_PASSWORD
        )

    def test_i18n_view(self):
        self.client.login(username=self.TEST_USERNAME,
                          password=self.TEST_PASSWORD)
        response = self.client.get('/savings/')
        self.assertRedirects(response, '/en/savings/', target_status_code=302)
        response = self.client.get('/savings/passbook/')
        self.assertRedirects(response, self.url)

    def test_index_view(self):
        self.client.login(username=self.TEST_USERNAME,
                          password=self.TEST_PASSWORD)
        response = self.client.get('/en/savings/')
        self.assertRedirects(response, self.url)

    def test_passbook_view(self):
        self.client.login(username=self.TEST_USERNAME,
                          password=self.TEST_PASSWORD)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertSequenceEqual(
            response.context['object_list'], [
                self.closed_passbook,
                self.today_passbook,
                self.this_week_passbook,
                self.this_month_passbook,
                self.next_month_passbook,
                self.next_year_passbook,
            ]
        )
        self.assertIsInstance(response.context['form'], PassbookSearchForm)

    def test_passbook_view_filter_open(self):
        self.client.login(username=self.TEST_USERNAME,
                          password=self.TEST_PASSWORD)
        response = self.client.get(self.url + '?is_open=2')
        self.assertEqual(response.status_code, 200)
        self.assertSequenceEqual(
            response.context['object_list'], [
                self.today_passbook,
                self.this_week_passbook,
                self.this_month_passbook,
                self.next_month_passbook,
                self.next_year_passbook,
            ]
        )

    def test_passbook_view_filter_close(self):
        self.client.login(username=self.TEST_USERNAME,
                          password=self.TEST_PASSWORD)
        response = self.client.get(self.url + '?is_open=3')
        self.assertEqual(response.status_code, 200)
        self.assertSequenceEqual(
            response.context['object_list'], [
                self.closed_passbook,
            ]
        )

    def test_passbook_view_filter_today(self):
        self.client.login(username=self.TEST_USERNAME,
                          password=self.TEST_PASSWORD)
        response = self.client.get(self.url + '?upcoming=' +
                                   self.today.strftime('%Y-%m-%d'))
        expected_object_list = [self.today_passbook]
        if self.today.month < (self.today + timedelta(days=1)).month:
            expected_object_list.append(self.this_month_passbook)
        self.assertEqual(response.status_code, 200)
        self.assertSequenceEqual(
            response.context['object_list'], expected_object_list)

    def test_passbook_view_filter_by_date(self):
        self.client.login(username=self.TEST_USERNAME,
                          password=self.TEST_PASSWORD)
        response = self.client.get(
            self.url + "?upcoming=%s-12-31" % (self.today.year + 2))
        self.assertEqual(response.status_code, 200)
        self.assertSequenceEqual(
            response.context['object_list'], [
                self.today_passbook,
                self.this_week_passbook,
                self.this_month_passbook,
                self.next_month_passbook,
                self.next_year_passbook,
            ]
        )

    def test_passbook_view_filter_by_invalid_date(self):
        self.client.login(username=self.TEST_USERNAME,
                          password=self.TEST_PASSWORD)
        response = self.client.get(self.url + '?upcoming=2016-31-12')
        self.assertEqual(response.status_code, 200)
        self.assertSequenceEqual(
            response.context['object_list'], [
                self.closed_passbook,
                self.today_passbook,
                self.this_week_passbook,
                self.this_month_passbook,
                self.next_month_passbook,
                self.next_year_passbook,
            ]
        )


class PassbookDeleteViewTest(TestCase):
    TEST_USERNAME = 'test'
    TEST_PASSWORD = 'testpassword'

    def setUp(self):
        today = datetime.today()
        self.passbook = Passbook.objects.create(
            number="001",
            account_number="001",
            amount=10000000,
            period=1,
            period_type=2,
            rate=5.0,
            start_date=today,
            stop_date=today + timedelta(days=31),
            is_open=True,
            notes="Note"
        )
        self.user = User.objects.create_user(
            username=self.TEST_USERNAME,
            password=self.TEST_PASSWORD
        )
        self.user.user_permissions.add(
            Permission.objects.get(codename='delete_passbook'))

    def test_get_request(self):
        self.client.login(username=self.TEST_USERNAME,
                          password=self.TEST_PASSWORD)
        response = self.client.get(reverse('savings:passbook_delete',
                                           args=(self.passbook.id, )))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Are you sure?')

    def test_post_request(self):
        self.client.login(username=self.TEST_USERNAME,
                          password=self.TEST_PASSWORD)
        response = self.client.post(reverse('savings:passbook_delete',
                                            args=(self.passbook.id, )))
        self.assertRedirects(response, reverse('savings:passbook_list'))


class PassbookWithdrawViewTest(TestCase):
    TEST_USERNAME = 'test'
    TEST_PASSWORD = 'testpassword'

    def setUp(self):
        self.passbook = Passbook.objects.create(
            number="001",
            account_number="001",
            amount=10000000,
            period=1,
            period_type=2,
            rate=5.0,
            start_date=datetime(2016, 5, 6).date(),
            stop_date=datetime(2016, 6, 6).date(),
            is_open=True,
            notes="Note"
        )
        self.user = User.objects.create_user(
            username=self.TEST_USERNAME,
            password=self.TEST_PASSWORD
        )
        self.user.user_permissions.add(
            Permission.objects.get(codename='change_passbook'))
        self.user.user_permissions.add(
            Permission.objects.get(codename='add_withdraw'))

    def test_get_request_without_querystring(self):
        self.client.login(username=self.TEST_USERNAME,
                          password=self.TEST_PASSWORD)
        response = self.client.get(reverse('savings:passbook_withdraw'))
        self.assertEqual(response.status_code, 400)

    def test_get_request(self):
        self.client.login(username=self.TEST_USERNAME,
                          password=self.TEST_PASSWORD)
        response = self.client.get(
            reverse('savings:passbook_withdraw') + '?date=2016-06-07')
        self.assertEqual(response.status_code, 200)
        self.assertSequenceEqual(
            response.context['object_list'], [self.passbook])
        self.assertIsInstance(response.context['form'], PassbookWithdrawForm)
        self.assertEqual(response.context['origin'], 10000000)
        self.assertEqual(response.context['interest'], 41832)

    def test_post_request(self):
        self.client.login(username=self.TEST_USERNAME,
                          password=self.TEST_PASSWORD)
        response = self.client.post(
            reverse('savings:passbook_withdraw'), {'date': '2016-06-07'})
        self.passbook.refresh_from_db()
        self.assertRedirects(response, reverse('savings:passbook_list'))
        self.assertEqual(self.passbook.is_open, False)
        withdraw = Withdraw.objects.latest('id')
        self.assertEqual(withdraw.amount, 10041832)
        self.assertEqual(withdraw.date, datetime(2016, 6, 7).date())
        self.assertEqual(withdraw.is_open, True)
