import pandas as pd


def process_weather_data1(input_file_path, output_file_path):
    # CSV 파일 불러오기
    df = pd.read_csv(input_file_path)

    # 'PCP' 및 'SNO' 열에서 '강수없음' 및 '적설없음'을 0으로 대체
    df.loc[df['category'] == 'PCP', 'fcstValue'] = df.loc[df['category'] == 'PCP', 'fcstValue'].replace('강수없음', 0)
    df.loc[df['category'] == 'SNO', 'fcstValue'] = df.loc[df['category'] == 'SNO', 'fcstValue'].replace('적설없음', 0)

    # Convert 'fcstValue' to numeric
    df['fcstValue'] = pd.to_numeric(df['fcstValue'], errors='coerce')

    # 'PCP'에 대한 추가 처리
    df.loc[(df['category'] == 'PCP') & (df['fcstValue'] < 1.0), 'fcstValue'] = 0.5
    df.loc[(df['category'] == 'PCP') & (df['fcstValue'] >= 50.0), 'fcstValue'] = 50.0

    # 'SNO'에 대한 추가 처리
    df.loc[(df['category'] == 'SNO') & (df['fcstValue'] < 1.0), 'fcstValue'] = 0.5
    df.loc[(df['category'] == 'SNO') & (df['fcstValue'] >= 5.0), 'fcstValue'] = 5.0

    # 데이터프레임을 fcstDate 및 fcstTime의 고유한 조합 단위로 변환
    df_pivoted = df.pivot(index=['fcstDate', 'fcstTime'], columns='category', values='fcstValue').reset_index()

    # mm 또는 cm 단위 삭제
    df_pivoted['PCP'] = df_pivoted['PCP'].astype(str).str.extract('(\d+.\d+|\d+)').astype(float)
    df_pivoted['SNO'] = df_pivoted['SNO'].astype(str).str.extract('(\d+.\d+|\d+)').astype(float)

    # 결과를 새로운 CSV 파일로 저장
    df_pivoted.to_csv(output_file_path, index=False)

    print(f"처리된 데이터가 {output_file_path}에 저장되었습니다.")



