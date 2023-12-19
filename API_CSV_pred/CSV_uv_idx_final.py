import pandas as pd

def process_uv_data_2(input_csv_path, output_csv_path):
    # CSV 파일 읽기
    df = pd.read_csv(input_csv_path, parse_dates=['time'])

    # 시간대를 KST로 변경
    df['time'] = df['time'].dt.strftime('%Y-%m-%d %H:%M:%S') + '+09:00'

    # 'time' 열을 DatetimeIndex로 설정
    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)

    # DatetimeIndex로 변환 후 3시간 간격 데이터를 1시간 간격으로 채우기
    df_resampled = df.resample('H').ffill().reset_index()

    # 결과를 새로운 CSV 파일로 저장
    df_resampled.to_csv(output_csv_path, index=False)

    print(f"새로운 CSV 파일이 생성되었습니다: {output_csv_path}")


