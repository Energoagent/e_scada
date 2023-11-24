from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

from rest_framework.response import Response
from rest_framework.views import APIView

from openpyxl import load_workbook
import xml.etree.ElementTree as ET

import requests
from requests.exceptions import HTTPError

def server(request):
    return render(request, 'server.html', 
        context = {
            'data_from_view': 'ESA SCADA',
            'context': 'server',
            }
        )

def about(request):
    request.session['floor_id'] = 2,
    request.session['unit_id'] = 214,
    request.session.modified = True
    return render(request, 'index.html', 
        context = {
            'data_from_view': 'ESA SCADA', 
            }
        )
def report_import(request):
    if request.method == 'GET':
        floor_id = request.session['floor_id']
        unit_id = request.session['unit_id']
    return redirect('../')

def report(request):
    if request.method == 'GET':
        floor_id = request.session['floor_id']
        unit_id = request.session['unit_id']
        return render(request, 'report.html', 
            context = {
                'data_from_view': 'ESA SCADA', 
                'context': 'report',
                'is_paginated' : 'true',
                'page_number' : '1',
                'floor_id': str(floor_id),
                'unit_id': str(unit_id),
                'contextmenu': {
                    'Импорт': 'formmethod=GET formaction=../import/'},
               }
            )

def graf(request):
    if request.method == 'GET':
        floor_id = request.session['floor_id']
        unit_id = request.session['unit_id']
        graf_number = int(request.GET.get('page_number'))
        graf_change = request.GET.get('page_change')
        match graf_change:
            case 'to_home': graf_number = 1
            case 'to_end': graf_number = 10
            case '+1': 
                graf_number = graf_number + 1
                if graf_number > 10: graf_number = 10
            case '-1': 
                graf_number = graf_number - 1
                if graf_number < 1: graf_number = 1
        request.session['unit_id'] = unit_id
        request.session.modified = True
        return render(request, 'graf.html', 
            context = {
                'data_from_view': 'ESA SCADA', 
                'context': 'graf',
                'is_paginated' : 'true',
                'page_number' : str(graf_number),
                'floor_id': str(floor_id),
                'unit_id': str(unit_id),
               }
            )
    else:
        return render(request, 'index.html', 
            context = {
                'data_from_view': 'invalid HTTP method',
                }
            )

def floor(request):
    if request.method == 'GET':
        floor_number = int(request.GET.get('page_number'))
        floor_change = request.GET.get('page_change')
        match floor_change:
            case 'to_home': floor_number = 1
            case 'to_end': floor_number = 3
            case '+1': 
                floor_number = floor_number + 1
                if floor_number > 3: floor_number = 3
            case '-1': 
                floor_number = floor_number - 1
                if floor_number < 1: floor_number = 1
        request.session['floor_id'] = floor_number
        request.session.modified = True
        context = {
            'data_from_view': 'ESA SCADA', 
            'context': 'floor',
            'is_paginated': 'true',
            'floor_id': floor_number,
            }
        match floor_number:
            case 1:
                context['page_number'] = str(floor_number)
                return render(request, 'common.html', context = context)
            case 2:
                context['page_number'] = str(floor_number)
                return render(request, 'floor2.html', context = context)
            case 3:
                context['page_number'] = str(floor_number)
                return render(request, 'floor3.html', context = context)
        return render(request, 'index.html', 
            context = {
                'data_from_view': 'floor not found', 
                'context': 'floor',
                }
            )
    else:
        return render(request, 'index.html', 
            context = {
                'data_from_view': 'invalid HTTP method', 
                }
            )

class Processor(APIView):
    def get(self, request):
        if request.method == 'GET':
            return Response({'TestData': 'TestData'})
        return Response({'Error': 'invalid HTTP method'})

class ParameterFloor2View(APIView):
    def get(self, request):
        if request.method == 'GET':
            page_number = request.session['floor_id']
            try:
                resp = requests.post('http://192.168.22.252:8686/parameter/',
                    timeout = 20,
                    params = {'page': str(page_number)})
            except Exception as e:
                print('EXEPTION:', e)
            else:
                if resp != None: 
                    parameters = resp.json()
#                    print('DEBUG:', resp.headers)
                    print('DEBUG:', resp.content)
#                    print('DEBUG:', resp.json())
                    parameters = resp.json()
                    return Response({'parameters': parameters})
        return Response({'Error': 'HTTP error'})

class ParameterGrafView(APIView):
    def get(self, request):
        if request.method == 'GET':
            try:
                resp = requests.post('http://192.168.22.252:8686/parameter/',
                    timeout = 1,
                    data = {'name': 'mbdV214'})
            except Exception as e:
                print('EXEPTION:', e)
            else:
                if resp != None: 
                    parameters = resp.json()
                    return Response({'parameters': parameters})
        return Response({'Error': 'HTTP error'})

