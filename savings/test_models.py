from datetime import datetime, timedelta

from django.test import TestCase

from .models import Passbook, Withdraw


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
            start_date=datetime(2016, 6, 6).date(),
            stop_date=datetime(2016, 8, 6).date(),
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

    def test_interest_on_withdraw_month_passbook_on_time(self):
        self.assertEqual(self.month_passbook.interest_on_withdraw(
            self.month_passbook.stop_date), self.month_passbook.interest())

    def test_interest_on_withdraw_month_passbook_overpass_small(self):
        self.assertEqual(self.month_passbook.interest_on_withdraw(
            self.month_passbook.stop_date + timedelta(days=10)), 84991)

    def test_interest_on_withdraw_month_passbook_overpass_large(self):
        self.assertEqual(self.month_passbook.interest_on_withdraw(
            self.month_passbook.stop_date + timedelta(days=70)), 168865)

    def test_interest_on_withdraw_week_passbook_on_time(self):
        self.assertEqual(self.week_passbook.interest_on_withdraw(
            self.week_passbook.stop_date), self.week_passbook.interest())

    def test_interest_on_withdraw_week_passbook_overpass_small(self):
        self.assertEqual(self.week_passbook.interest_on_withdraw(
            self.week_passbook.stop_date + timedelta(days=10)), 20825)

    def test_interest_on_withdraw_week_passbook_overpass_large(self):
        self.assertEqual(self.week_passbook.interest_on_withdraw(
            self.week_passbook.stop_date + timedelta(days=20)), 39383)

    def test_get_info_week_passbook_on_time(self):
        date = self.week_passbook.stop_date
        self.assertEqual(
            self.week_passbook._get_info(date),
            self.week_passbook._get_info_week(date)
        )
        base, in_period, out_period = self.week_passbook._get_info(date)
        self.assertEqual(base, 365 / 7)
        self.assertEqual(in_period, 1)
        self.assertEqual(out_period, 0)

    def test_get_info_week_passbook_overpass_small(self):
        date = self.week_passbook.stop_date + timedelta(days=10)
        base, in_period, out_period = self.week_passbook._get_info(date)
        self.assertEqual(base, 365 / 7)
        self.assertEqual(in_period, 1)
        self.assertEqual(out_period, 10)

    def test_get_info_week_passbook_overpass_large(self):
        date = self.week_passbook.stop_date + timedelta(days=20)
        base, in_period, out_period = self.week_passbook._get_info(date)
        self.assertEqual(base, 365 / 7)
        self.assertEqual(in_period, 2)
        self.assertEqual(out_period, 6)

    def test_get_info_month_passbook_on_time(self):
        date = self.month_passbook.stop_date
        self.assertEqual(
            self.month_passbook._get_info(date),
            self.month_passbook._get_info_month(date)
        )
        base, in_period, out_period = self.month_passbook._get_info(date)
        self.assertEqual(base, 12)
        self.assertEqual(in_period, 1)
        self.assertEqual(out_period, 0)

    def test_get_info_month_passbook_overpass_small(self):
        date = self.month_passbook.stop_date + timedelta(days=10)
        base, in_period, out_period = self.month_passbook._get_info(date)
        self.assertEqual(base, 12)
        self.assertEqual(in_period, 1)
        self.assertEqual(out_period, 10)

    def test_get_info_month_passbook_overpass_large(self):
        date = self.month_passbook.stop_date + timedelta(days=70)
        base, in_period, out_period = self.month_passbook._get_info(date)
        self.assertEqual(base, 12)
        self.assertEqual(in_period, 2)
        self.assertEqual(out_period, 9)


class WithdrawTest(TestCase):

    def setUp(self):
        self.today = datetime.today().date()
        self.passbook = Passbook.objects.create(
            number="001",
            account_number="001",
            amount=10000000,
            period=2,
            period_type=2,
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

    def test_update_passbook_does_not_change_withdraw(self):
        self.passbook.is_open = False
        self.passbook.save()
        self.withdraw.refresh_from_db()
        self.assertEqual(self.withdraw.is_open, True)

    def test_create_other_momdal_does_not_change_withdraws(self):
        Withdraw.objects.create(
            amount=10000000,
            date=self.today,
            is_open=True
        )
        self.withdraw.refresh_from_db()
        self.assertEqual(self.withdraw.is_open, True)

    def test_create_closed_passbook_does_not_change_withdraws(self):
        Passbook.objects.create(
            number="002",
            account_number="002",
            amount=10000000,
            period=2,
            period_type=2,
            rate=5.0,
            start_date=self.today,
            stop_date=self.today,
            is_open=False,
            notes="Note"
        )
        self.withdraw.refresh_from_db()
        self.assertEqual(self.withdraw.is_open, True)

    def test_create_open_passbook_close_withdraws(self):
        Passbook.objects.create(
            number="003",
            account_number="003",
            amount=10000000,
            period=2,
            period_type=2,
            rate=5.0,
            start_date=self.today,
            stop_date=self.today,
            is_open=True,
            notes="Note"
        )
        self.withdraw.refresh_from_db()
        self.assertEqual(self.withdraw.is_open, False)
