# -*- coding: utf-8 -*-

import locale
import os
import pytz
import responses
import tweepy

from datetime import datetime
from django.test import TestCase
from core.utils import crs_to_date

from core.models import BloodGroup, Log

from mock import mock

from .utils import MockPhantomJS


class UtilsTest(TestCase):

    def test_date_formatter(self):
        date_last_update = crs_to_date('Aggiornato a\xa0mercoledì 03 agosto 2016\xa0alle\xa012:50')
        locale.setlocale(locale.LC_TIME, "it_IT.UTF-8")
        date_expected = pytz.timezone('Europe/Rome').localize(
            datetime.strptime('03 agosto 2016 12:50', '%d %B %Y %H:%M')
        )
        locale.resetlocale(locale.LC_TIME)
        self.assertEqual(date_last_update, date_expected)

    def test_date_formatter_failing(self):
        self.assertRaises(ValueError, crs_to_date, 'Wrong value')
