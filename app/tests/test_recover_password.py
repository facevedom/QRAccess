from django.test import TestCase 
from django.core import mail

from django.contrib.auth.models import User
from app.models import Company
from app.models import RecoveryLink

class RecoverPasswordTest(TestCase):

    def setUp(self):
        User.objects.create_user(username='testcompany', password='password')
        Company.objects.create(
            name='testcompany',
            email='contact@test.com.co',
            address='123 6th St. Melbourne',
            telephone='12345678'
        )

    def test_password_recovery_renders_correct_html(self):
        response = self.client.get('/company/recover_password/')
        self.assertContains(response, 'Recover your password')
        self.assertTemplateUsed(response, 'company/recover_password.html')

    def test_password_recovery_requires_existing_email(self):
        form = RecoverCompanyPasswordForm(data={'email': 'unexisting@email.com'})
        self.assertFalse(form.is_valid())

    def test_password_recovery_send_email_after_POST(self):
        self.client.post('/company/recover_password/', data={'email': 'contact@test.com.co'})
        self.assertEquals(len(mail.outbox), 1)
        mail_sent = mail.outbox[0]
        self.assertEquals(mail_sent.subject, 'QRAccess - Recover your password')
        self.assertIn('contact@test.com.co', mail_sent.to)
