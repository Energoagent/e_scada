from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

from rest_framework.response import Response
from rest_framework.views import APIView

def about(request):
    return render(request, 'index.html', 
        context = {
            'data_from_view': 'ESA SCADA', 
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
