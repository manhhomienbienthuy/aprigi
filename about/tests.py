from django.test import TestCase
from django.core.urlresolvers import reverse

class AboutTest(TestCase):
    def assertView(self, name):
        self.assertContains(self.client.get(reverse('about:%s' %name)), 'Aprigi')

    def test_about_this_site(self):
        self.assertView('this_site')

    def test_about_us(self):
        self.assertView('us')

    def test_about_privacy(self):
        self.assertView('us')

    def test_about_terms(self):
        self.assertView('terms')

    def test_about_contact(self):
        self.assertView('contact')
