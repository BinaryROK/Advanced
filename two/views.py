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

    file_path = f'gens/{selected_date}.csv'
    return render(request, 'two/two.html', {'file_path': file_path, 'selected_date': selected_date})


# 기존의 chart_data_2 함수 수정
def chart_data_2(request, selected_date):
    file_path = f'gens/{selected_date}.csv'

    df = read_csv_file(file_path)

    # 시간과 예측값을 가져와서 리스트로 변환
    labels = df['time'].tolist()
    data = df['amount'].tolist()
    chart_data = {
        'labels': labels,
        'data': data,
    }

    return JsonResponse(chart_data)


