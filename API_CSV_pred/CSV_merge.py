import pandas as pd

class DataMerger:
    def __init__(self, weather_path, uv_idx_path, sun_data_path, output_path):
        self.weather_path = weather_path
        self.uv_idx_path = uv_idx_path
        self.sun_data_path = sun_data_path
        self.output_path = output_path

    def merge_data(self):
        print("데이터 병합 중...")

        # CSV 파일 읽기
        weather_data = pd.read_csv(self.weather_path)
        uv_idx_data = pd.read_csv(self.uv_idx_path)
        sun_data = pd.read_csv(self.sun_data_path)

        # 'time' 열을 기준으로 세 데이터프레임을 병합
        merged_data = pd.merge(weather_data, uv_idx_data, on='time')
        merged_data = pd.merge(merged_data, sun_data, on='time')

        # 'time' 열을 인덱스로 설정
        merged_data.set_index('time', inplace=True)

        # 중복된 'time' 열 제거
        merged_data = merged_data.loc[~merged_data.index.duplicated(keep='first')]

        # 새로운 CSV 파일로 저장
        merged_data.to_csv(self.output_path)

        print(f'데이터 병합 완료. 결과는 {self.output_path}에 저장되었습니다.')
