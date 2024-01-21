from django.urls import path

from . import views

app_name = 'expediente'


urlpatterns = [
    path('', views.expediente_detail, name='detail'),
    path('get_id', views.get_expediente_id, name='get_expediente_id')
]
