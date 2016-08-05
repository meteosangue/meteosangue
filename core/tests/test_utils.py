# -*- coding: utf-8 -*-
import os
import responses

from datetime import datetime
from django.test import TestCase
from core.utils import crs_to_date, update_blood_groups

from core.models import BloodGroup, Log


class UtilsTest(TestCase):

    def test_date_formatter(self):
        date_last_update = crs_to_date('Aggiornato a\xa0mercoledì 03 agosto 2016\xa0alle\xa012:50')
        date_expected = datetime.strptime('03 agosto 2016 12:50', '%d %B %Y %H:%M')
        self.assertEqual(date_last_update, date_expected)

    def test_date_formatter_failing(self):
        self.assertRaises(ValueError, crs_to_date, 'Wrong value')

    @responses.activate
    def test_blood_groups_fetcher(self):
        mock_body = open(os.path.join(os.path.dirname(__file__), 'data', 'crs_page.html')).read()
        responses.add(responses.GET, 'https://web2.e.toscana.it/crs/meteo/',
                  body=mock_body, status=200,
                  content_type='text/html; charset=UTF-8')
        self.assertEqual(len(BloodGroup.objects.all()), 0)
        update_blood_groups()
        self.assertEqual(len(BloodGroup.objects.all()), 8)
        update_blood_groups()
        self.assertEqual(len(BloodGroup.objects.all()), 8)

    @responses.activate
    def test_do_not_duplicate_logs(self):
        mock_body = open(os.path.join(os.path.dirname(__file__), 'data', 'crs_page.html')).read()
        responses.add(responses.GET, 'https://web2.e.toscana.it/crs/meteo/',
                  body=mock_body, status=200,
                  content_type='text/html; charset=UTF-8')
        self.assertEqual(len(Log.objects.all()), 0)
        update_blood_groups()
        self.assertEqual(len(Log.objects.all()), 1)
        update_blood_groups()
        self.assertEqual(len(Log.objects.all()), 1)


    @responses.activate
    def test_update_blood_status(self):
        self.assertEqual(len(Log.objects.all()), 0)
        self.assertEqual(len(BloodGroup.objects.all()), 0)

        mock_body = open(os.path.join(os.path.dirname(__file__), 'data', 'crs_page.html')).read()
        responses.add(responses.GET, 'https://web2.e.toscana.it/crs/meteo/',
                  body=mock_body, status=200,
                  content_type='text/html; charset=UTF-8')

        update_blood_groups()
        self.assertEqual(len(Log.objects.all()), 1)
        first_time = Log.objects.all()[0].datetime
        self.assertEqual(len(BloodGroup.objects.all()), 8)
        self.assertEqual(BloodGroup.objects.get(groupid='ABN').status, 'U')

        responses.reset()

        mock_body = open(os.path.join(os.path.dirname(__file__), 'data', 'crs_page_update.html')).read()
        responses.add(responses.GET, 'https://web2.e.toscana.it/crs/meteo/',
                  body=mock_body, status=200,
                  content_type='text/html; charset=UTF-8')


        update_blood_groups()
        self.assertEqual(len(Log.objects.all()), 1)
        second_time = Log.objects.all()[0].datetime
        self.assertEqual(len(BloodGroup.objects.all()), 8)
        self.assertEqual(BloodGroup.objects.get(groupid='ABN').status, 'E')

        self.assertNotEqual(first_time, second_time)
