# two/views.py
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
import pandas as pd
from django.http import HttpResponse

# two/views.py에 read_csv_file 함수 정의 추가
def read_csv_file(file_path):
    df = pd.read_csv(file_path)
    return df

# two/views.py
def two(request, selected_date='default_date_value'):
    if selected_date == 'default_date_value':
        # 디폴트 값에 해당하는 처리
        return HttpResponse("Please select a date.")

    # 기존 데이터 파일 경로
    file_path = f'Data/zaraData/{selected_date}.csv'

    # 기존 데이터
    df = read_csv_file(file_path)

    # 새로운 데이터 파일 경로 (여기서는 임의로 예시를 제공하므로 경로를 실제 데이터 파일 경로로 수정해야 합니다.)
    new_file_path = f'Data/predicted/{selected_date}.csv'

    # 새로운 데이터
    new_df = read_csv_file(new_file_path)

    # URL을 생성하여 전달
    two_url = reverse('two', args=[selected_date])
    new_chart_data_url = reverse('chart_data_2', args=[selected_date])

    # 기존 데이터와 새로운 데이터를 따로 그리기 위해 두 개의 데이터를 전달
    return render(request, 'two/two.html', {'file_path': file_path, 'selected_date': selected_date, 'df': df, 'new_df': new_df, 'two_url': two_url, 'new_chart_data_url': new_chart_data_url})
