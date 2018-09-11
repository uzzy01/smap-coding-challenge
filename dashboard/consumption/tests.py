# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client
from django.urls import reverse
from django.db import models
from .models import user_data, consumption_data
from django.core.management import call_command
from django.conf import settings
from datetime import datetime
import os, pytz

# Create your tests here.

# Test for views

class views_test(TestCase):

    def setUp(self):
        self.client = Client()

    def test_summary_status_code(self):
        response = self.client.get("/summary/")
        self.assertEquals(response.status_code, 200)

    def test_summary_by_name(self):
        response = self.client.get(reverse('summary'))
        self.assertEquals(response.status_code, 200)

    def test_detail_status_code(self):
        response = self.client.get("/detail/asdf/")
        self.assertEquals(response.status_code, 404)

# Test models

class models_test(TestCase):

    def setUp(self):
        user = [ user_data( user_id=1, area='a2', tariff='t1' ), 
                user_data( user_id=2, area='a4', tariff='t3' ) ]

        user_data.objects.bulk_create(user)

        self.user_1 = user_data.objects.get(user_id=1)
        self.user_2 = user_data.objects.get(user_id=2)

    def test_user_info(self):
        self.assertEquals(self.user_1.area, 'a2')

    def test_consumption_aggregation(self):
        consumption = [
            consumption_data(user_id=self.user_1,
                             datetime=pytz.utc.localize(datetime.strptime('2017-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')),
                             consumption='30'),
            consumption_data(user_id=self.user_1,
                             datetime=pytz.utc.localize(datetime.strptime('2017-01-01 00:30:00', '%Y-%m-%d %H:%M:%S')),
                             consumption='60'),
            consumption_data(user_id=self.user_2,
                             datetime=pytz.utc.localize(datetime.strptime('2017-01-01 00:30:00', '%Y-%m-%d %H:%M:%S')),
                             consumption='20')
        ]

        consumption_data.objects.bulk_create(consumption)

        sum_value = 90
        avg_value = 45
        query = consumption_data.objects.filter(user_id=1).values('user_id')
        query = query.annotate(sum=models.Sum('consumption'), 
                               avg=models.Avg('consumption'))

        self.assertEquals(query[0]['sum'], sum_value)
        self.assertEquals(query[0]['avg'], avg_value)

# Test import cmd

class command_test(TestCase):
    
    def test_import(self):
        # Test to see if invalid path throws error
        path = os.path.join(settings.USER_DATA_DIR, 'user_data.csv')
        call_command('import', path)
