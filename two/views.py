# two/views.py

from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
from django.http import HttpResponse

import csv

# two/views.py에 read_csv_file 함수 정의 추가
def read_csv_file(file_path):
    df = pd.read_csv(file_path)
    return df

# two/views.py
def two(request, selected_date='default_date_value'):
    if selected_date == 'default_date_value':
        # 디폴트 값에 해당하는 처리
        return HttpResponse("Please select a date.")

    file_path = f'Data/zaraData/{selected_date}.csv'
    return render(request, 'two/two.html', {'file_path': file_path, 'selected_date': selected_date})


# 기존의 chart_data_2 함수 수정
def chart_data_2(request, selected_date):
    actual_file_path = f'Data/zaraData/{selected_date}.csv'
    predicted_file_path = f'Data/predicted/{selected_date}.csv'

    actual_df = read_csv_file(actual_file_path)
    predicted_df = read_csv_file(predicted_file_path)

    # 실제 및 예측 값에 대한 시간과 양 데이터 추출
    actual_labels = actual_df['time'].tolist()
    actual_data = actual_df['amount'].tolist()

    predicted_labels = predicted_df['time'].tolist()
    predicted_data = predicted_df['amount'].tolist()

    chart_data = {
        'labels': {
            'actual': actual_labels,
            'predicted': predicted_labels,
        },
        'data': {
            'actual': actual_data,
            'predicted': predicted_data,
        },
    }

    return JsonResponse(chart_data)


