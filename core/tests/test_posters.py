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
from core.posters import telegram_status, tweet_status, facebook_status
from core.posters_register import posters_register
from core.tasks import fetch_and_update

from mock import mock

from .utils import MockPhantomJS


class PostersTest(TestCase):

    @mock.patch('core.main.webdriver.PhantomJS', autospec = True)
    @mock.patch('core.posters.facebook.GraphAPI', autospec = True)
    def test_poster_with_tags_facebook(self, facebook_mock, phantom_driver):
        mock_body = open(os.path.join(os.path.dirname(__file__), 'data', 'crs_page.html')).read()

        posters_register._posters = []
        posters_register.register_poster(facebook_status, 'facebook_done')

        m = mock.Mock()

        m.put_photo.side_effect = mock.Mock(id='1')

        facebook_mock.return_value = m

        phantom_driver.return_value = MockPhantomJS(mock_body)

        self.assertEqual(len(Log.objects.all()), 0)

        meteo_fake_status = '🚨 Emergenza: A+ , A- , O+ , O- , B- , AB- , AB+\n'
        meteo_upload_fake = os.path.join(os.path.dirname(__file__), 'data', 'meteo_fake_upload.png')

        facebook_status(meteo_fake_status, meteo_upload_fake)

        self.assertEqual(m.put_wall_post.call_count, 0)
        self.assertEqual(m.put_photo.call_count, 1)
        self.assertEqual(
            m.put_photo.call_args[1]['tags'],
            '[{"tag_uid": "andrea.stagi"}, {"tag_uid": "patrick.arminio"}]'
        )


    @mock.patch('core.main.webdriver.PhantomJS', autospec = True)
    @mock.patch('core.posters.tweepy.OAuthHandler', autospec = True)
    @mock.patch('core.posters.tweepy.API', autospec = True)
    def test_poster_with_mentions_twitter(self, tweepy_mock, tweepy_oauth_mock, phantom_driver):
        mock_body = open(os.path.join(os.path.dirname(__file__), 'data', 'crs_page.html')).read()

        posters_register._posters = []
        posters_register.register_poster(tweet_status, 'twitter_done')

        m = mock.Mock()
        m.update_with_media.return_value = mock.Mock(id='1')

        tweepy_mock.return_value = m

        phantom_driver.return_value = MockPhantomJS(mock_body)

        fetch_and_update()

        self.assertEqual(m.update_status.call_count, 1)
        self.assertEqual(m.update_with_media.call_count, 1)
        m.update_status.assert_called_with(
            '@4stagi @patrick91 Nuovo bollettino meteo ⬆',
            in_reply_to_status_id='1'
        )


    @mock.patch('core.main.webdriver.PhantomJS', autospec = True)
    @mock.patch('core.posters.tweepy.OAuthHandler', autospec = True)
    @mock.patch('core.posters.tweepy.API', autospec = True)
    @mock.patch('core.posters.telepot.Bot', autospec = True)
    @mock.patch('core.posters.facebook.GraphAPI', autospec = True)
    def test_post_on_exception(self, facebook_mock, telegram_mock, tweepy_mock, tweepy_oauth_mock, phantom_driver):

        # Twitter

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

        # Telegram

        Log.objects.all().delete()

        posters_register._posters = []
        posters_register.register_poster(telegram_status, 'telegram_done')

        m = mock.Mock()
        m.sendMessage.side_effect = telepot.exception.TelepotException('Error on Telegram')

        telegram_mock.return_value = m

        phantom_driver.return_value = MockPhantomJS(mock_body)

        self.assertEqual(len(Log.objects.all()), 0)
        mock_body = open(os.path.join(os.path.dirname(__file__), 'data', 'crs_page.html')).read()

        fetch_and_update()

        self.assertFalse(Log.objects.all()[0].telegram_done)
        self.assertEqual(m.sendMessage.call_count, 1)
        self.assertEqual(m.sendPhoto.call_count, 1)

        # Facebook

        Log.objects.all().delete()

        posters_register._posters = []
        posters_register.register_poster(facebook_status, 'facebook_done')

        m = mock.Mock()

        m.put_photo.side_effect = Exception('Error on Facebook')

        facebook_mock.return_value = m

        phantom_driver.return_value = MockPhantomJS(mock_body)

        self.assertEqual(len(Log.objects.all()), 0)
        mock_body = open(os.path.join(os.path.dirname(__file__), 'data', 'crs_page.html')).read()

        fetch_and_update()

        self.assertFalse(Log.objects.all()[0].facebook_done)
        self.assertEqual(m.put_wall_post.call_count, 0)
        self.assertEqual(m.put_photo.call_count, 1)
