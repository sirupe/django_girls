from django.urls import path
from . import views
app_name = 'polls'
urlpatterns = [
    path('entrance/', views.entrance, name='entrance')
]
