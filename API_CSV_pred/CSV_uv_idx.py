import pandas as pd
from datetime import datetime, timedelta

def process_uv_data_1(input_file_path, output_file_path):
    # CSV 파일 불러오기
    df = pd.read_csv(input_file_path)

    # time 열을 datetime 형식으로 변환
    df['time'] = pd.to_datetime(df['time'], format='%Y%m%d%H')

    # 새로운 데이터프레임 생성
    data_list = []

    # 시간에 따라 데이터 추가
    for i in range(len(df)):
        current_time = df.loc[i, 'time']
        for j in range(26):
            new_time = current_time + timedelta(hours=j * 3)
            new_uv_idx = df.loc[i, f'h{j * 3}']
            data_list.append({'time': new_time, 'uv_idx': new_uv_idx})

    # 결과 데이터프레임 생성
    new_df = pd.DataFrame(data_list)

    # 결과 데이터프레임 출력 또는 저장
    new_df.to_csv(output_file_path, index=False)


