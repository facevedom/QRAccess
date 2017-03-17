from django.test import TestCase

class HomeTest(TestCase):

    def test_home(self):
        """Tests the home page."""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'app/index.html')