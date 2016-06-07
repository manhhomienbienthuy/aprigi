from datetime import datetime

from django.test import TestCase

from .forms import PassbookForm


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
