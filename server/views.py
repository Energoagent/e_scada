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
            parameter = request.GET.get('parameter')
            match parameter:
                case 'Pressure':
                    pressure = datetime.now().time().second
        return Response({'Pressure': str(pressure)})