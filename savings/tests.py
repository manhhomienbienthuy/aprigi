from calendar import monthrange
from datetime import datetime, timedelta
from unittest import mock

from django.core.urlresolvers import reverse
from django.test import TestCase

from .forms import PassbookForm, PassbookSearchForm
from .models import Passbook


def faketoday():
    return datetime(2016, 6, 6)


class PassbookTest(TestCase):

    def setUp(self):
        self.today = datetime.today().date()
        self.month_passbook = Passbook.objects.create(
            number="001",
            account_number="001",
            amount=10000000,
            period=2,
            period_type=2,
            rate=5.0,
            start_date=self.today,
            stop_date=self.today + timedelta(days=61),
            is_open=True,
            notes="Note"
        )
        self.week_passbook = Passbook.objects.create(
            number="002",
            account_number="002",
            amount=10000000,
            period_type=1,
            period=2,
            rate=5.0,
            start_date=self.today,
            stop_date=self.today + timedelta(days=14),
            is_open=True,
            notes="Note"
        )
        self.closed_passbook = Passbook.objects.create(
            number="003",
            account_number="003",
            amount=10000000,
            period_type=2,
            period=1,
            rate=5.0,
            start_date=self.today,
            stop_date=self.today,
            is_open=False,
            notes="Note"
        )

    def test_interest_closed_passbook(self):
        self.assertEqual(self.closed_passbook.interest(), None)

    def test_interest_month_passbook(self):
        self.assertEqual(self.month_passbook.interest(), 83333)

    def test_interest_week_passbook(self):
        self.assertEqual(self.week_passbook.interest(), 19178)

    def test_interest_on_withdraw_closed_passbook(self):
        self.assertEqual(self.closed_passbook.interest_on_withdraw(
            self.closed_passbook.stop_date), None)

    def test_interest_on_withdraw_month_passbook(self):
        self.assertEqual(self.month_passbook.interest_on_withdraw(
            self.month_passbook.stop_date), self.month_passbook.interest())
        self.assertEqual(self.month_passbook.interest_on_withdraw(
            self.month_passbook.stop_date + timedelta(days=10)), 84991)

    def test_interest_on_withdraw_week_passbook(self):
        self.assertEqual(self.week_passbook.interest_on_withdraw(
            self.week_passbook.stop_date), self.week_passbook.interest())
        self.assertEqual(self.week_passbook.interest_on_withdraw(
            self.week_passbook.stop_date + timedelta(days=10)), 20825)

    def test_get_info_week_passbook(self):
        date = self.week_passbook.stop_date
        self.assertEqual(
            self.week_passbook._get_info(date),
            self.week_passbook._get_info_week(date)
        )
        base, in_period, out_period = self.week_passbook._get_info(date)
        self.assertEqual(base, 365 / 7)
        self.assertEqual(in_period, 1)
        self.assertEqual(out_period, 0)
        date = self.week_passbook.stop_date + timedelta(days=10)
        base, in_period, out_period = self.week_passbook._get_info(date)
        self.assertEqual(base, 365 / 7)
        self.assertEqual(in_period, 1)
        self.assertEqual(out_period, 10)
        date = self.week_passbook.stop_date + timedelta(days=20)
        base, in_period, out_period = self.week_passbook._get_info(date)
        self.assertEqual(base, 365 / 7)
        self.assertEqual(in_period, 2)
        self.assertEqual(out_period, 6)

    def test_get_info_month_passbook(self):
        date = self.month_passbook.stop_date
        self.assertEqual(
            self.month_passbook._get_info(date),
            self.month_passbook._get_info_month(date)
        )
        base, in_period, out_period = self.month_passbook._get_info(date)
        self.assertEqual(base, 12)
        self.assertEqual(in_period, 1)
        self.assertEqual(out_period, 0)
        date = self.month_passbook.stop_date + timedelta(days=10)
        base, in_period, out_period = self.month_passbook._get_info(date)
        self.assertEqual(base, 12)
        self.assertEqual(in_period, 1)
        self.assertEqual(out_period, 10)


class PassbookViewTest(TestCase):

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

    def test_i18n_view(self):
        response = self.client.get('/savings/')
        self.assertRedirects(response, '/en/savings/', target_status_code=302)
        response = self.client.get('/savings/passbook/')
        self.assertRedirects(response, self.url)

    def test_index_view(self):
        response = self.client.get('/en/savings/')
        self.assertRedirects(response, self.url)

    @mock.patch('django.utils.timezone.now', faketoday)
    def test_passbook_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        expected_object_list = [
            self.closed_passbook,
            self.today_passbook,
            self.this_week_passbook,
            self.this_month_passbook,
            self.next_month_passbook,
            self.next_year_passbook,
        ]
        self.assertSequenceEqual(
            response.context['object_list'],
            expected_object_list
        )
        self.assertIsInstance(response.context['form'], PassbookSearchForm)
        self.assertEqual(response.context['thisweek'], '2016-06-13')
        self.assertEqual(response.context['thismonth'], '2016-06-30')
        self.assertEqual(response.context['origin'], 50000000)
        self.assertEqual(response.context['interest'], 208335)

    @mock.patch('django.utils.timezone.now', faketoday)
    def test_passbook_view_filter_open(self):
        response = self.client.get(self.url + '?is_open=2')
        self.assertEqual(response.status_code, 200)
        expected_object_list = [
            self.today_passbook,
            self.this_week_passbook,
            self.this_month_passbook,
            self.next_month_passbook,
            self.next_year_passbook,
        ]
        self.assertSequenceEqual(
            response.context['object_list'],
            expected_object_list
        )
        self.assertIsInstance(response.context['form'], PassbookSearchForm)
        self.assertEqual(response.context['thisweek'], '2016-06-13')
        self.assertEqual(response.context['thismonth'], '2016-06-30')
        self.assertEqual(response.context['origin'], 50000000)
        self.assertEqual(response.context['interest'], 208335)

    @mock.patch('django.utils.timezone.now', faketoday)
    def test_passbook_view_filter_close(self):
        response = self.client.get(self.url + '?is_open=3')
        self.assertEqual(response.status_code, 200)
        expected_object_list = [
            self.closed_passbook,
        ]
        self.assertSequenceEqual(
            response.context['object_list'],
            expected_object_list
        )
        self.assertIsInstance(response.context['form'], PassbookSearchForm)
        self.assertEqual(response.context['thisweek'], '2016-06-13')
        self.assertEqual(response.context['thismonth'], '2016-06-30')
        self.assertEqual(response.context['origin'], 0)
        self.assertEqual(response.context['interest'], 0)

    @mock.patch('django.utils.timezone.now', faketoday)
    def test_passbook_view_filter_today(self):
        response = self.client.get(self.url + '?upcoming=' +
                                   self.today.strftime('%Y-%m-%d'))
        expected_object_list = [self.today_passbook]
        if self.today.month < (self.today + timedelta(days=1)).month:
            expected_object_list.append(self.this_month_passbook)
        self.assertEqual(response.status_code, 200)
        self.assertSequenceEqual(
            response.context['object_list'], expected_object_list)
        self.assertIsInstance(response.context['form'], PassbookSearchForm)
        self.assertEqual(response.context['thisweek'], '2016-06-13')
        self.assertEqual(response.context['thismonth'], '2016-06-30')
        self.assertEqual(response.context['origin'], sum(
            obj.amount for obj in expected_object_list))
        self.assertEqual(response.context['interest'], sum(
            obj.interest() or 0 for obj in expected_object_list))

    @mock.patch('django.utils.timezone.now', faketoday)
    def test_passbook_view_filter_by_date(self):
        response = self.client.get(
            self.url + "?upcoming=%s-12-31" % (self.today.year + 2))
        self.assertEqual(response.status_code, 200)
        expected_object_list = [
            self.today_passbook,
            self.this_week_passbook,
            self.this_month_passbook,
            self.next_month_passbook,
            self.next_year_passbook,
        ]
        self.assertSequenceEqual(
            response.context['object_list'],
            expected_object_list
        )
        self.assertIsInstance(response.context['form'], PassbookSearchForm)
        self.assertEqual(response.context['thisweek'], '2016-06-13')
        self.assertEqual(response.context['thismonth'], '2016-06-30')
        self.assertEqual(response.context['origin'], 50000000)
        self.assertEqual(response.context['interest'], 208335)

    @mock.patch('django.utils.timezone.now', faketoday)
    def test_passbook_view_filter_by_invalid_date(self):
        response = self.client.get(self.url + '?upcoming=2016-31-12')
        self.assertEqual(response.status_code, 200)
        expected_object_list = [
            self.closed_passbook,
            self.today_passbook,
            self.this_week_passbook,
            self.this_month_passbook,
            self.next_month_passbook,
            self.next_year_passbook,
        ]
        self.assertSequenceEqual(
            response.context['object_list'],
            expected_object_list
        )
        self.assertIsInstance(response.context['form'], PassbookSearchForm)
        self.assertEqual(response.context['thisweek'], '2016-06-13')
        self.assertEqual(response.context['thismonth'], '2016-06-30')
        self.assertEqual(response.context['origin'], 50000000)
        self.assertEqual(response.context['interest'], 208335)


class PassbookFormTest(TestCase):

    def setUp(self):
        self.valid_data = {
            'number': '001',
            'account_number': '001',
            'amount': 10,
            'period_type': 2,
            'period': 1,
            'rate': 5.0,
            'start_date': '2016-06-01',
            'stop_date': '2016-07-01',
            'is_open': True,
            'notes': 'Note'
        }

    def test_submit_success(self):
        form = PassbookForm(self.valid_data)
        self.assertTrue(form.is_valid)
        instance = form.save()
        self.assertEqual(instance.number, '001')
        self.assertEqual(instance.account_number, '001')
        self.assertEqual(instance.amount, 10)
        self.assertEqual(instance.period_type, 2)
        self.assertEqual(instance.period, 1)
        self.assertEqual(instance.rate, 5.0)
        self.assertEqual(instance.start_date, datetime(2016, 6, 1).date())
        self.assertEqual(instance.stop_date, datetime(2016, 7, 1).date())
        self.assertEqual(instance.is_open, True)
        self.assertEqual(instance.notes, 'Note')


class PassbookDeleteViewTest(TestCase):

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

    def test_get_request(self):
        response = self.client.get(reverse('savings:passbook_delete',
                                           args=(self.passbook.id, )))
        self.assertContains(response, 'Are you sure?')

    def test_post_request(self):
        response = self.client.post(reverse('savings:passbook_delete',
                                            args=(self.passbook.id, )))
        self.assertRedirects(response, reverse('savings:passbook_list'))
