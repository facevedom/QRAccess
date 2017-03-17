from django.test import TestCase


class ContactTest(TestCase):

    def test_contact(self):
        """Tests the contact page."""
        response = self.client.get('/contact')
        self.assertTemplateUsed(response, 'app/contact.html')
