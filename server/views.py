from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

from rest_framework.response import Response
from rest_framework.views import APIView

from openpyxl import load_workbook

parameters = {}

try:
    wb = load_workbook('config/parameters.xlsx')
except Exception as e: 
    print('EXCEPTION:', e)
sheet = wb.active
for i in range(2, sheet.max_row):
    parameters[sheet.cell(row = i, column = 1).value] = str(sheet.cell(row = i, column = 2).value)

def about(request):
    return render(request, 'index.html', 
        context = {
            'data_from_view': 'ESA SCADA', 
            }
        )

def server(request):
    return render(request, 'server.html', 
        context = {
            'data_from_view': 'ESA SCADA SERVER', 
            }
        )

def floor(request):
    return render(request, 'floor.html', 
        context = {
            'data_from_view': 'ESA SCADA SERVER', 
            }
        )

class Processor(APIView):
    def get(self, request):
        if request.method == 'GET':
            prmType = request.GET.get('prmType')
            match prmType:
                case 'Pressure':
                    pressure = datetime.now().time().second
                    return Response({'Pressure': str(pressure)})
            match prmType:
                case 'Temperature':
                    temperature = datetime.now().time().minute
                    return Response({'Temperature': str(temperature)})
            match prmType:
                case 'Humidity':
                    humidity = datetime.now().time().second
                    return Response({'Humidity': str(humidity)})
        return Response({'Error': 'undefined parameter type'})

class ParameterFloorView(APIView):
    def get(self, request):
        if request.method == 'GET':
            return Response({'parameters':parameters})
        else:
            return Response({'Error': 'invalid HTTP method'})

