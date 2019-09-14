from django.core import mail
from django.contrib.auth.models import User
from dajngo.urls importreverse
from django.test import TestCase

class PasswordResetMailTests(TestCase):
	def setUp(self):
		User.objects.create_user(username = 'abhi', email = 'abhiSaphire@gmail.com', password = 'helloabhi')
		self.response = self.client.post(reverse('password_reset'), {'email' : 'abhiSaphire@gmail.com'})
		self.email = mail.outbox[0]

	def test_email_subject(self):
		self.assertEqual('[CHARCHA] Please reset your password', self.email.subject)

	def test_email_body(self):
		context = self.response.context
		token = context.get('token')
		uid = context.get('uid')
		password_reset_token_url = reverse('password_reset_confirm', kwargs={
			'uidb64': uid,
			'token': token
		})
		self.assertIn(password_reset_token_url, self.email.body)
		self.assertIn('abhi', self.email.body)
		self.assertIn('abhiSaphire@gmail.com', self.email.body)

	def test_email_to(self):
		self.assertEqual(['abhiSaphire@gmail.com',], self.email.to)