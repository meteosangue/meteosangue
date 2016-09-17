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
from core.posters import telegram_status, tweet_status
from core.posters_register import posters_register
from core.tasks import fetch_and_update

from mock import mock

from .utils import MockPhantomJS


class PostersTest(TestCase):

    @mock.patch('core.main.webdriver.PhantomJS', autospec = True)
    @mock.patch('core.posters.tweepy.OAuthHandler', autospec = True)
    @mock.patch('core.posters.tweepy.API', autospec = True)
    @mock.patch('core.posters.telepot.Bot', autospec = True)
    def test_twitter_post_on_exception(self, telegram_mock, tweepy_mock, tweepy_oauth_mock, phantom_driver):

        mock_body = open(os.path.join(os.path.dirname(__file__), 'data', 'crs_page.html')).read()

        posters_register._posters = []
        posters_register.register_poster(tweet_status, 'twitter_done')

        m = mock.Mock()
        m.update_with_media.side_effect = tweepy.TweepError('Error on Twitter')

        tweepy_mock.return_value = m

        phantom_driver.return_value = MockPhantomJS(mock_body)

        self.assertEqual(len(Log.objects.all()), 0)
        mock_body = open(os.path.join(os.path.dirname(__file__), 'data', 'crs_page.html')).read()

        fetch_and_update()

        self.assertFalse(Log.objects.all()[0].twitter_done)
        self.assertEqual(m.update_status.call_count, 0)
        self.assertEqual(m.update_with_media.call_count, 1)

    @mock.patch('core.main.webdriver.PhantomJS', autospec = True)
    @mock.patch('core.posters.tweepy.OAuthHandler', autospec = True)
    @mock.patch('core.posters.tweepy.API', autospec = True)
    @mock.patch('core.posters.telepot.Bot', autospec = True)
    def test_telegram_post_on_exception(self, telegram_mock, tweepy_mock, tweepy_oauth_mock, phantom_driver):

        mock_body = open(os.path.join(os.path.dirname(__file__), 'data', 'crs_page.html')).read()

        posters_register._posters = []
        posters_register.register_poster(telegram_status, 'twitter_done')

        m = mock.Mock()
        m.sendMessage.side_effect = telepot.exception.TelepotException('Error on Telegram')

        telegram_mock.return_value = m

        phantom_driver.return_value = MockPhantomJS(mock_body)

        self.assertEqual(len(Log.objects.all()), 0)
        mock_body = open(os.path.join(os.path.dirname(__file__), 'data', 'crs_page.html')).read()

        fetch_and_update()

        self.assertFalse(Log.objects.all()[0].telegram_done)
        self.assertEqual(m.sendMessage.call_count, 1)
        self.assertEqual(m.sendPhoto.call_count, 0)
