from django.test import TestCase


class ViewTest(TestCase):

    def test_about(self):
        """Tests the about page."""
        response = self.client.get('/about')
        self.assertTemplateUsed(response, 'app/about.html')
