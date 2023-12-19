import pandas as pd
from datetime import timedelta

def process_weather_data2(input_file_path, output_file_path):
    # CSV 파일 읽기
    df = pd.read_csv(input_file_path)

    # fcstDate와 fcstTime을 합쳐서 datetime 형태의 time 열 생성
    df['time'] = pd.to_datetime(df['fcstDate'].astype(str) + df['fcstTime'].astype(str).str.zfill(4), format='%Y%m%d%H%M')

    # 시간대를 KST로 변경하면서 형식 유지
    df['time'] = df['time'].dt.strftime('%Y-%m-%d %H:%M:%S') + '+09:00'

    # 열 이름 변경
    df.rename(columns={'PCP': 'rain', 'REH': 'humidity', 'SNO': 'snow', 'TMP': 'temp', 'VEC': 'wind_dir', 'WSD': 'wind_speed'}, inplace=True)

    # 열의 순서 조정
    df = df[['time', 'temp', 'humidity', 'wind_speed', 'wind_dir', 'rain', 'snow']]

    # wind_speed에 3.6 곱하기
    df['wind_speed'] *= 3.6

    # snow에 10 곱하기
    df['snow'] *= 10

    # CSV 파일로 저장
    df.to_csv(output_file_path, index=False)

    print(f"새로운 CSV 파일이 생성되었습니다: {output_file_path}")

