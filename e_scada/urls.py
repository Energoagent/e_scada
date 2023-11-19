
from django.contrib import admin
from django.urls import path, include, re_path

from server import views

urlpatterns = [
    path('server/processor/', views.Processor.as_view()),
    path('floor/processor/', views.ParameterFloorView.as_view()),
    path('', views.about),
    path('server/', views.server),
    path('floor/', views.floor),
    path('about/', views.about),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]
