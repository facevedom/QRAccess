from django.test import TestCase
from django.contrib.auth.models import User
from django.core import mail

from app.models import Company
from app.forms import CompanyForm

class CompanyFormTest(TestCase):

    def setUp(self):
        pass

    def test_company_registration_render_correct_html(self):
        response = self.client.get('/company/registration/')
        self.assertContains(response, 'registration')
        self.assertTemplateUsed(response, 'company/company_registration.html')

    def test_company_registration_correct_company_form(self):
        form_data = {
            'email': 'contact@test.com.co', 
            'telephone': '12345678', 
            'name': 'testcompany', 
            'address': '123 6th St. Melbourne', 
            'password': 'password'
        }
        form = CompanyForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_company_registration_required_fields_empty(self):
        form_data = {'email': '', 'telephone': '', 'name': '', 'address': '', 'password': ''}
        form = CompanyForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_company_registration_incorrect_email_format(self):
        form_data = {
            'email': 'bad_email_format', 
            'telephone': '12345678', 
            'name': 'testcompany', 
            'address': '123 6th St. Melbourne', 
            'password': 'password'
        }
        form = CompanyForm(data=form_data)
        self.assertFalse(form.is_valid())
        

    def test_company_registration_correct_phone_format(self):
        form_data = {
            'email': 'contact@test.com.co', 
            'telephone': '123abc', 
            'name': 'testcompany', 
            'address': '123 6th St. Melbourne', 
            'password': 'password'
        }
        form = CompanyForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_company_registration_requires_unique_username(self):
        self.company = Company.objects.create(name='testcompany', email='contact@test.com.co', telephone='2761234')
        form_data = {
            'email': 'contact@test.com.co', 
            'telephone': '12345678', 
            'name': 'testcompany', 
            'address': '123 6th St. Melbourne', 
            'password': 'password'
        }
        form = CompanyForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_company_registration_saves_a_new_company_after_POST(self):
        self.client.post(
            '/company/registration/',
            data={
                'email': 'contact@test.com.co', 
                'telephone': '12345678', 
                'name': 'testcompany', 
                'address': '123 6th St. Melbourne', 
                'password': 'password'       
            }
        )
        self.assertEqual(Company.objects.count(), 1)
        new_company = Company.objects.first()
        self.assertEqual(new_company.name, 'testcompany')
        self.assertEqual(User.objects.count(), 1)
        new_user = User.objects.first()
        self.assertEqual(new_user.username, 'testcompany')

    def test_company_registration_send_validation_email_after_POST(self):
        self.client.post(
            '/company/registration/',
            data={
                'email': 'contact@test.com.co', 
                'telephone': '12345678', 
                'name': 'testcompany', 
                'address': '123 6th St. Melbourne', 
                'password': 'password'       
            }
        )

        self.assertEqual(len(mail.outbox), 1)
        mail_sent = mail.outbox[0]
        self.assertEqual(mail_sent.subject, 'QRAccess - Please confirm your email address')
        self.assertIn('contact@test.com.co', mail_sent.to)
