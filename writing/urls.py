from django.urls import path
from . import views
app_name = 'polls'
urlpatterns = [
    path('entrance/', views.entrance, name='entrance'),
    path('writing/write_form', views.write_form, name='write_form'),
    path('write', views.write, name='write')
]
