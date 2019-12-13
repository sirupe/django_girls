from django.urls import path

from writing.views import EntranceView, WriteView

app_name = 'polls'
urlpatterns = [
    path('', EntranceView.as_view(), name=''),
    path('write', WriteView.as_view(), name='write')
]
