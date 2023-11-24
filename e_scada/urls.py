
from django.contrib import admin
from django.urls import path, include, re_path

from server import views

urlpatterns = [
    path('server/processor/', views.Processor.as_view()),
    path('floor/processor/', views.ParameterFloor2View.as_view()),
    path('graf/processor/', views.ParameterGrafView.as_view()),
    path('floor/', views.floor),
    path('', views.about),
    path('server/', views.server),
    path('graf/', views.graf),
    path('report/', views.report),
    path('report/import/', views.report_import),
    path('about/', views.about),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]
