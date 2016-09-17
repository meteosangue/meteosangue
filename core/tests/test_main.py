# -*- coding: utf-8 -*-

import os
import pytz
import responses
import telepot
import tweepy

from datetime import datetime
from django.test import TestCase
from core.exceptions import MeteoSangueException
from core.main import update_blood_groups, get_blood_group_list
from core.models import BloodGroup, Log
from core.posters_register import posters_register
from core.tasks import fetch_and_update

from mock import mock

from .utils import MockPhantomJS


class MainTest(TestCase):

    @mock.patch('core.main.webdriver.PhantomJS', autospec = True)
    def test_blood_groups_fetcher(self, phantom_driver):
        mock_body = open(os.path.join(os.path.dirname(__file__), 'data', 'crs_page.html')).read()
        phantom_driver.return_value = MockPhantomJS(mock_body)
        self.assertEqual(len(BloodGroup.objects.all()), 0)
        update_blood_groups()
        self.assertEqual(len(BloodGroup.objects.all()), 8)
        update_blood_groups()
        self.assertEqual(len(BloodGroup.objects.all()), 8)

    @mock.patch('core.main.webdriver.PhantomJS', autospec = True)
    def test_do_not_duplicate_logs(self, phantom_driver):
        mock_body = open(os.path.join(os.path.dirname(__file__), 'data', 'crs_page.html')).read()
        phantom_driver.return_value = MockPhantomJS(mock_body)
        self.assertEqual(len(Log.objects.all()), 0)
        update_blood_groups()
        self.assertEqual(len(Log.objects.all()), 1)
        update_blood_groups()
        self.assertEqual(len(Log.objects.all()), 1)

    @mock.patch('core.main.webdriver.PhantomJS', autospec = True)
    def test_update_blood_status(self, phantom_driver):

        self.assertEqual(len(Log.objects.all()), 0)
        self.assertEqual(len(BloodGroup.objects.all()), 0)

        mock_body = open(os.path.join(os.path.dirname(__file__), 'data', 'crs_page.html')).read()
        phantom_driver.return_value = MockPhantomJS(mock_body)

        update_blood_groups()
        self.assertEqual(len(Log.objects.all()), 1)
        first_time = Log.objects.all()[0].datetime
        self.assertEqual(len(BloodGroup.objects.all()), 8)
        self.assertEqual(BloodGroup.objects.get(groupid='AB-').status, 'U')

        mock_body = open(os.path.join(os.path.dirname(__file__), 'data', 'crs_page_update.html')).read()
        phantom_driver.return_value = MockPhantomJS(mock_body)

        update_blood_groups()
        self.assertEqual(len(Log.objects.all()), 1)
        second_time = Log.objects.all()[0].datetime
        self.assertEqual(len(BloodGroup.objects.all()), 8)
        self.assertEqual(BloodGroup.objects.get(groupid='AB-').status, 'E')

        self.assertNotEqual(first_time, second_time)

    def test_get_blood_group_list(self):
        BloodGroup.objects.create(groupid='B+', status='Z')
        BloodGroup.objects.create(groupid='B-', status='U')
        BloodGroup.objects.create(groupid='0-', status='U')
        blood_groups = BloodGroup.objects.all()
        self.assertEqual(
            get_blood_group_list(blood_groups, '⚫️', 'Z', 'Emergenza'),
            '⚫️ Emergenza: B+\n'
        )
        self.assertEqual(
            get_blood_group_list(blood_groups, '🔴', 'U', 'Urgenza'),
            '🔴 Urgenza: B- , 0-\n'
        )
        self.assertEqual(
            get_blood_group_list(blood_groups, '💛', 'E', 'Eccedenza'),
            ''
        )

    @mock.patch('core.main.webdriver.PhantomJS', autospec = True)
    @mock.patch('core.main.tweet_status', autospec = True)
    @mock.patch('core.main.telegram_status', autospec = True)
    def test_do_not_post_on_twitter_two_times(self, telegram_status, tweet_status, phantom_driver):

        posters_register._posters = []
        posters_register.register_poster(tweet_status, 'twitter_done')
        posters_register.register_poster(telegram_status, 'telegram_done')

        self.assertEqual(len(Log.objects.all()), 0)
        mock_body = open(os.path.join(os.path.dirname(__file__), 'data', 'crs_page.html')).read()

        phantom_driver.return_value = MockPhantomJS(mock_body)

        fetch_and_update()
        self.assertEqual(tweet_status.call_count, 1)

        fetch_and_update()
        self.assertEqual(tweet_status.call_count, 1)

    @mock.patch('core.main.webdriver.PhantomJS', autospec = True)
    @mock.patch('core.main.tweet_status', autospec = True)
    @mock.patch('core.main.telegram_status', autospec = True)
    def test_retry_on_twitter_exception(self, telegram_status, tweet_status, phantom_driver):

        posters_register._posters = []
        posters_register.register_poster(tweet_status, 'twitter_done')
        posters_register.register_poster(telegram_status, 'telegram_done')

        self.assertEqual(len(Log.objects.all()), 0)
        mock_body = open(os.path.join(os.path.dirname(__file__), 'data', 'crs_page.html')).read()

        phantom_driver.return_value = MockPhantomJS(mock_body)

        tweet_status.side_effect = MeteoSangueException('Error on Twitter')
        fetch_and_update()
        self.assertTrue(not Log.objects.all()[0].twitter_done)

        tweet_status.side_effect = None
        fetch_and_update()
        self.assertTrue(Log.objects.all()[0].twitter_done)

    @mock.patch('core.main.webdriver.PhantomJS', autospec = True)
    @mock.patch('core.main.tweet_status', autospec = True)
    @mock.patch('core.main.telegram_status', autospec = True)
    def test_retry_on_telegram_exception(self, telegram_status, tweet_status, phantom_driver):

        posters_register._posters = []
        posters_register.register_poster(tweet_status, 'twitter_done')
        posters_register.register_poster(telegram_status, 'telegram_done')

        self.assertEqual(len(Log.objects.all()), 0)
        mock_body = open(os.path.join(os.path.dirname(__file__), 'data', 'crs_page.html')).read()

        phantom_driver.return_value = MockPhantomJS(mock_body)

        telegram_status.side_effect = MeteoSangueException('Error on Telegram')
        fetch_and_update()
        self.assertTrue(not Log.objects.all()[0].telegram_done)

        telegram_status.side_effect = None
        fetch_and_update()
        self.assertTrue(Log.objects.all()[0].telegram_done)
