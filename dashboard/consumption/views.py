# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import user_data, consumption_data

# Create your views here.

def summary(request):
    try:
        all_users = user_data.objects.all().order_by('user_id')
        total_consumption = consumption_data.get_total_consumption();
        context = {
            'user_data' : all_users,
            'total_consumption' : total_consumption
        }
    except Exception as e:
        raise Http404(str(e))

    return render(request, 'consumption/summary.html', context)

def detail(request, user_id):
    user_detail = get_object_or_404(user_data, pk=user_id)
    user_consumption = consumption_data.get_user_consumption(user_id)
    aggregated_user_data = consumption_data.aggregated_user_data(user_id)
    context = {
        'user_detail' : user_detail,
        'user_consumption' : user_consumption,
        'aggregated_user_data' : aggregated_user_data
    }
    
    return render(request, 'consumption/detail.html', context)
