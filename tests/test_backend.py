# -*- coding: utf-8 -*-
import unittest

from django.core.mail import EmailMessage
from exchangelib import Credentials
from exchangelib.errors import AutoDiscoverFailed, AutoDiscoverError

from django_exchange.backend import ExchangeEmailBackend


class TestEmailBackend(unittest.TestCase):

    def setUp(self) -> None:
        self.host = 'mail.example.com'
        self.port = 25
        self.username = 'JohnDoe'
        self.password = 'Passw0rd!'
        self.fail_silently = False
        self.domain = 'example-domain.de'

    def test_init(self):

        mail_backend = ExchangeEmailBackend(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            fail_silently=self.fail_silently,
            domain=self.domain
        )

        self.assertEqual(mail_backend.host, self.host)
        self.assertEqual(mail_backend.port, self.port)
        self.assertEqual(mail_backend.username, self.username)
        self.assertEqual(mail_backend.password, self.password)
        self.assertEqual(mail_backend.fail_silently, self.fail_silently)
        self.assertEqual(mail_backend.domain, self.domain)

    def test_open(self):
        mail_backend = ExchangeEmailBackend(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            fail_silently=self.fail_silently,
            domain=self.domain
        )

        mail_backend.open()
        credentials = mail_backend.credentials
        self.assertEqual(credentials.username, f'{self.host}\\{self.username}')
        self.assertEqual(credentials.password, self.password)

    def test_double_open(self):
        mail_backend = ExchangeEmailBackend(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            fail_silently=self.fail_silently,
            domain=self.domain
        )

        self.assertTrue(mail_backend.open())
        credentials = mail_backend.credentials
        self.assertEqual(credentials.username, f'{self.host}\\{self.username}')
        self.assertEqual(credentials.password, self.password)
        self.assertFalse(mail_backend.open())
        self.assertEqual(credentials.username, f'{self.host}\\{self.username}')
        self.assertEqual(credentials.password, self.password)

    def test_early_close(self):
        mail_backend = ExchangeEmailBackend(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            fail_silently=self.fail_silently,
            domain=self.domain
        )
        self.assertEqual(mail_backend.credentials, None)
        mail_backend.close()
        self.assertEqual(mail_backend.credentials, None)

    def test_close(self):
        mail_backend = ExchangeEmailBackend(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            fail_silently=self.fail_silently,
            domain=self.domain
        )
        self.assertEqual(mail_backend.credentials, None)
        mail_backend.open()
        self.assertIsInstance(mail_backend.credentials, Credentials)
        mail_backend.close()
        self.assertEqual(mail_backend.credentials, None)


class TestEmailBackendSend(TestEmailBackend):

    def test_send_mail_no_recipients(self):
        mail_backend = ExchangeEmailBackend(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            fail_silently=self.fail_silently,
            domain=self.domain
        )

        message = EmailMessage(
            subject='test',
            body='Test \n Body',
            from_email='from@example.com'
        )
        message.encoding = 'utf-8'

        self.assertEqual(mail_backend.send_messages([message]), 0)

    def test_send_mail(self):
        mail_backend = ExchangeEmailBackend(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            fail_silently=self.fail_silently,
            domain=self.domain
        )

        message = EmailMessage(
            subject='test',
            body='Test \n Body',
            from_email='from@example.com',
            to=['me@example.com']
        )
        message.encoding = 'utf-8'
        with self.assertRaises(AutoDiscoverFailed):
            mail_backend.send_messages([message])
