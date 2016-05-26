from calendar import monthrange
from datetime import datetime, timedelta

from django.test import TestCase

from .models import Passbook


class PassbookViewTest(TestCase):

    def setUp(self):
        self.today = datetime.today()
        self.closed_passbook = Passbook.objects.create(
            number="001",
            account_number="001",
            amount=10,
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
            amount=10,
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
            amount=10,
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
            amount=10,
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
            amount=10,
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
            amount=10,
            period_type=2,
            period=1,
            rate=5.0,
            start_date=self.today,
            stop_date=self.today + timedelta(days=367),
            is_open=True,
            notes="Note"
        )

    def test_passbook_view(self):
        response = self.client.get('/savings/')
        self.assertEqual(response.status_code, 200)
        self.assertSequenceEqual(
            response.context['object_list'],
            [
                self.closed_passbook,
                self.today_passbook,
                self.this_week_passbook,
                self.this_month_passbook,
                self.next_month_passbook,
                self.next_year_passbook,
            ]
        )

    def test_passbook_view_filter_open(self):
        response = self.client.get('/savings/?is_open=1')
        self.assertEqual(response.status_code, 200)
        self.assertSequenceEqual(
            response.context['object_list'],
            [
                self.today_passbook,
                self.this_week_passbook,
                self.this_month_passbook,
                self.next_month_passbook,
                self.next_year_passbook,
            ]
        )

    def test_passbook_view_filter_close(self):
        response = self.client.get('/savings/?is_open=0')
        self.assertEqual(response.status_code, 200)
        self.assertSequenceEqual(
            response.context['object_list'],
            [
                self.closed_passbook,
            ]
        )

    def test_passbook_view_filter_today(self):
        response = self.client.get('/savings/?upcoming=today')
        expected_object_list = [self.today_passbook]
        if self.today.month < (self.today + timedelta(days=1)).month:
            expected_object_list.append(self.this_month_passbook)
        self.assertEqual(response.status_code, 200)
        self.assertSequenceEqual(
            response.context['object_list'], expected_object_list)

    def test_passbook_view_filter_thisweek(self):
        response = self.client.get('/savings/?upcoming=thisweek')
        expected_object_list = [
            self.today_passbook,
            self.this_week_passbook,
        ]
        if self.today.month < (self.today + timedelta(days=7)).month:
            expected_object_list.append(self.this_month_passbook)
        self.assertEqual(response.status_code, 200)
        self.assertSequenceEqual(
            response.context['object_list'], expected_object_list)

    def test_passbook_view_filter_thismonth(self):
        response = self.client.get('/savings/?upcoming=thismonth')
        expected_object_list = [self.today_passbook]
        if self.today.month == (self.today + timedelta(days=1)).month:
            expected_object_list.append(self.this_week_passbook)
        expected_object_list.append(self.this_month_passbook)
        self.assertEqual(response.status_code, 200)
        self.assertSequenceEqual(
            response.context['object_list'], expected_object_list)

    def test_passbook_view_filter_by_date(self):
        response = self.client.get(
            "/savings/?upcoming=%s-12-31" % (self.today.year + 2))
        self.assertEqual(response.status_code, 200)
        self.assertSequenceEqual(
            response.context['object_list'],
            [
                self.today_passbook,
                self.this_week_passbook,
                self.this_month_passbook,
                self.next_month_passbook,
                self.next_year_passbook,
            ]
        )

    def test_passbook_view_filter_by_invalid_date(self):
        response = self.client.get('/savings/?upcoming=2016-31-12')
        self.assertEqual(response.status_code, 200)
        self.assertSequenceEqual(
            response.context['object_list'],
            [
                self.closed_passbook,
                self.today_passbook,
                self.this_week_passbook,
                self.this_month_passbook,
                self.next_month_passbook,
                self.next_year_passbook,
            ]
        )
