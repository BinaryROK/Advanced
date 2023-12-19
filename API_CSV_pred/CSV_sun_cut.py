import pandas as pd

def process_sun_data_1(input_csv_path, output_csv_path):
    # CSV 파일을 데이터프레임으로 읽어오기
    df = pd.read_csv(input_csv_path)

    # 인덱스를 'locdate', 'azimuth', 'altitude'로 변경
    df = df.rename(columns={'ocdate': 'locdate'})
    df['locdate'] = pd.to_datetime(df['locdate'], format='%Y%m%d')  # Convert 'locdate' to datetime format
    df = df.melt(id_vars='locdate', var_name='time', value_name='value')

    # 시간(time)에서 시(hour)와 데이터 종류(type) 추출
    df[['type', 'hour']] = df['time'].str.split('_', expand=True)

    # 분 값 제거
    df['value'] = df['value'].apply(lambda x: int(x.split('˚')[0]))

    # 필요한 시간대(09, 12, 15, 18시)의 데이터만 선택
    selected_hours = ['09', '12', '15', '18']
    df_selected = df[df['hour'].isin(selected_hours)].copy()

    # 필요한 컬럼만 선택
    df_selected = df_selected[['locdate', 'hour', 'type', 'value']]

    # 피벗 테이블을 사용하여 최종 데이터프레임 생성
    df_pivoted = df_selected.pivot_table(index=['locdate', 'hour'], columns='type', values='value').reset_index()

    # 컬럼명 변경
    df_pivoted.columns = ['locdate', 'hour', 'altitude', 'azimuth']

    # 최종 데이터프레임을 CSV 파일로 저장
    df_pivoted.to_csv(output_csv_path, index=False)

    print(f'Data saved to {output_csv_path}')


