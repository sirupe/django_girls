from django.urls import path

from writing.views import EntranceView, WriteView, WritingListView, WritingView

app_name = 'polls'
urlpatterns = [
    path('', WritingListView.as_view(), name='index'),
    path('write', WriteView.as_view(), name='write'),
    path(r'(?P<pk>\d+)/$', WritingView.as_view(), name='writing')
]
