# two/views.py

from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
from django.http import HttpResponse

# 함수를 정의하여 CSV 파일 읽기
def read_csv_file(file_path):
    df = pd.read_csv(file_path)
    return df

def two(request, selected_date='default_date_value'):
    if selected_date == 'default_date_value':
        return HttpResponse("Please select a date.")

    zara_file_path = f'Data/zaraData/{selected_date}.csv'
    predicted_file_path = f'Data/predicted/{selected_date}.csv'

    return render(request, 'two/two.html', {
        'zara_file_path': zara_file_path,
        'predicted_file_path': predicted_file_path,
        'selected_date': selected_date
    })

def chart_data_2(request, selected_date):
    file_path = f'Data/zaraData/{selected_date}.csv'

    df = read_csv_file(file_path)

    labels = df['time'].tolist()
    data = df['amount'].tolist()
    chart_data = {
        'labels': labels,
        'data': data,
    }

    return JsonResponse(chart_data)

def new_chart_data(request, selected_date):
    file_path = f'Data/predicted/{selected_date}.csv'

    df = read_csv_file(file_path)

    labels = df['time'].tolist()
    data = df['amount'].tolist()
    chart_data = {
        'labels': labels,
        'data': data,
    }

    return JsonResponse(chart_data)


