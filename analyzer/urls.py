from django.urls import path
from . import views
from . import analysis_history

app_name = 'analyzer'
urlpatterns = [
    path('', views.index, name='index'),
    path('history', analysis_history.get_history, name='history'),
    path('delete/<int:id>', analysis_history.delete_history_by_id, name='delete')
]
