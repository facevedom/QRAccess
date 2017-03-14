from django.test import TestCase
from django.template.loader import render_to_string

import re
from datetime import datetime


class ViewTest(TestCase):
    """Tests for the application views."""

    @staticmethod
    def remove_csrf(html_code):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_regex, '', html_code)

    def test_home(self):
        """Tests the home page."""
        response = self.client.get('/')
        self.assertContains(response, 'Home Page', 1, 200)

        expected_html = render_to_string('app/index.html',
                                            {
                                                'title': 'Home Page',
                                                'year': datetime.now().year,
                                            }
                                        )
        self.assertEquals(self.remove_csrf(response.content.decode()), expected_html)

    def test_contact(self):
        """Tests the contact page."""
        response = self.client.get('/contact')
        self.assertContains(response, 'Contact', 3, 200)

        expected_html = render_to_string('app/contact.html',
                                            {
                                                'title': 'Contact',
                                                'message': 'Your contact page.',
                                                'year': datetime.now().year,
                                            }
                                        )
        self.assertEquals(self.remove_csrf(response.content.decode()), expected_html)

    def test_about(self):
        """Tests the about page."""
        response = self.client.get('/about')
        self.assertContains(response, 'About', 3, 200)

        expected_html = render_to_string('app/about.html',
                                            {
                                                'title': 'About',
                                                'message': 'Your application description page.',
                                                'year': datetime.now().year,
                                            }
                                        )
        self.assertEquals(self.remove_csrf(response.content.decode()), expected_html)
