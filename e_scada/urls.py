
from django.contrib import admin
from django.urls import path
from django.urls import path, include

from server import views

urlpatterns = [
    path('', views.about),
    path('processor', views.Processor.as_view()),
    path('about/', views.about, name = 'about'),
    path('admin/', admin.site.urls),
#    path('accounts/', include('django.contrib.auth.urls')),
]
