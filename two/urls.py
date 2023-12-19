# two/urls.py
from django.urls import path
from .views import two, chart_data_2, new_chart_data

urlpatterns = [
    path('<str:selected_date>/', two, name='two'),
    path('<str:selected_date>/chart_data/', chart_data_2, name='chart_data_2'),
    path('<str:selected_date>/new_chart_data/', new_chart_data, name='new_chart_data'),

    path('', two, {'selected_date': ''}, name='home'),  # 디폴트 값 설정
]


