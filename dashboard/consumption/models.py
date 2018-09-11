# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.functions import ExtractMonth
import calendar

class user_data(models.Model):
    user_id = models.IntegerField(primary_key=True)
    area = models.CharField(max_length=10)
    tariff = models.CharField(max_length=10)

    def __str__(self):
        return "User: {0}".format(self.user_id)

class consumption_data(models.Model):
    user_id = models.ForeignKey(user_data, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    consumption = models.FloatField()

    @classmethod
    def get_total_consumption(cls):
        #aggregate data, getting total users sum & avg - grouping by month
        record_set = consumption_data.objects.annotate(month=ExtractMonth('datetime')).values('month')
        record_set = record_set.annotate(sum=models.Sum('consumption'),
                                         avg=models.Avg('consumption'))
        record_set = record_set.order_by('month')
        
        return consumption_data.convert_month(record_set)

    @classmethod
    def get_user_consumption(cls,user_id):
        record_set = consumption_data.objects.filter(user_id=user_id).annotate(month=ExtractMonth('datetime')).values('month')
        record_set = record_set.annotate(sum=models.Sum('consumption'),
                                         avg=models.Avg('consumption'))

        return consumption_data.convert_month(record_set)

    @classmethod
    def aggregated_user_data(cls,user_id):
        record_set = consumption_data.objects.filter(user_id=user_id).values('user_id')
        record_set = record_set.annotate(sum=models.Sum('consumption'), 
                                         avg=models.Avg('consumption'))
          
        record_set = dict(user_id=record_set[0]['user_id'],
                          avg=round(record_set[0]['avg'],2),
                          sum=round(record_set[0]['sum'],2)
                    )

        return record_set

    def convert_month(rs):
        #Convert month number to month name for better visualization
        return [dict(month=calendar.month_name[record['month']],
                     sum=round(record['sum'],2),
                     avg=round(record['avg'],2)) for record in rs]