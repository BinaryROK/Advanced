import pandas as pd
import numpy as np

def interpolate_sun_data(input_csv_path, output_csv_path):
    # CSV 파일 불러오기
    df = pd.read_csv(input_csv_path)

    # 'locdate'와 'hour' 열을 합쳐 'time' 열 생성
    df['time'] = pd.to_datetime(df['locdate'] + ' ' + df['hour'].astype(str) + ':00:00')

    # 'locdate' 및 'hour' 열 삭제
    df.drop(['locdate', 'hour'], axis=1, inplace=True)

    # 'altitude' 열 이름을 'elevation'로 변경
    df.rename(columns={'altitude': 'elevation'}, inplace=True)

    # 빈 시간대를 생성
    all_hours = pd.date_range(start=df['time'].min().replace(hour=0), end=df['time'].max().replace(hour=23), freq='H')

    # 빈 시간대에 대한 데이터 프레임 생성
    full_df = pd.DataFrame(index=all_hours)

    # 기존 데이터 프레임과 병합
    full_df = pd.merge(full_df, df, left_index=True, right_on='time', how='left')

    # azimuth와 elevation이 NaN인 부분을 등차수열로 채우기
    full_df['azimuth'] = full_df['azimuth'].interpolate()
    full_df['elevation'] = full_df['elevation'].interpolate()

    # 00:00부터 08:00까지는 09:00의 값으로, 19:00부터 23:00까지는 18:00의 값으로 채우기
    full_df.loc[full_df['time'].dt.hour < 9, ['azimuth', 'elevation']] = full_df.loc[full_df['time'].dt.hour == 9, ['azimuth', 'elevation']].values
    full_df.loc[full_df['time'].dt.hour > 18, ['azimuth', 'elevation']] = full_df.loc[full_df['time'].dt.hour == 18, ['azimuth', 'elevation']].values

    # 열 순서 변경
    full_df = full_df[['time', 'azimuth', 'elevation']]

    # 'time' 열을 문자열로 변환하여 '+09:00' 추가
    full_df['time'] = full_df['time'].dt.strftime('%Y-%m-%d %H:%M:%S') + '+09:00'

    # 새로운 CSV 파일로 저장
    full_df.to_csv(output_csv_path, index=False)

    # 결과 확인
    print(f"Dataframe saved to {output_csv_path}")


