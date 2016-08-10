# -*- coding: utf-8 -*-
import os
import responses

from datetime import datetime
from django.test import TestCase
from core.utils import crs_to_date, update_blood_groups, get_blood_group_list

from core.models import BloodGroup, Log

from mock import mock

from .utils import MockPhantomJS

class UtilsTest(TestCase):

    def test_date_formatter(self):
        date_last_update = crs_to_date('Aggiornato a\xa0mercoledì 03 agosto 2016\xa0alle\xa012:50')
        date_expected = datetime.strptime('03 agosto 2016 12:50', '%d %B %Y %H:%M')
        self.assertEqual(date_last_update, date_expected)

    def test_date_formatter_failing(self):
        self.assertRaises(ValueError, crs_to_date, 'Wrong value')

    @mock.patch('core.utils.webdriver.PhantomJS', autospec = True)
    def test_blood_groups_fetcher(self, phantom_driver):
        mock_body = open(os.path.join(os.path.dirname(__file__), 'data', 'crs_page.html')).read()
        phantom_driver.return_value = MockPhantomJS(mock_body)
        self.assertEqual(len(BloodGroup.objects.all()), 0)
        update_blood_groups()
        self.assertEqual(len(BloodGroup.objects.all()), 8)
        update_blood_groups()
        self.assertEqual(len(BloodGroup.objects.all()), 8)

    @mock.patch('core.utils.webdriver.PhantomJS', autospec = True)
    def test_do_not_duplicate_logs(self, phantom_driver):
        mock_body = open(os.path.join(os.path.dirname(__file__), 'data', 'crs_page.html')).read()
        phantom_driver.return_value = MockPhantomJS(mock_body)
        self.assertEqual(len(Log.objects.all()), 0)
        update_blood_groups()
        self.assertEqual(len(Log.objects.all()), 1)
        update_blood_groups()
        self.assertEqual(len(Log.objects.all()), 1)

    @mock.patch('core.utils.webdriver.PhantomJS', autospec = True)
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
            '🔴 Urgenza: B- | 0-\n'
        )
        self.assertEqual(
            get_blood_group_list(blood_groups, '💛', 'E', 'Eccedenza'),
            ''
        )

