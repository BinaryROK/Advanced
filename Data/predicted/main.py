import pandas as pd
from datetime import timedelta, datetime
import API_weather
from CSV_weather_cut1 import process_weather_data1  # CSV_weather_cut1 모듈에서 함수를 가져옴
from CSV_weather_cut2 import process_weather_data2  # CSV_weather_cut2 모듈에서 함수를 가져옴
from API_uv_idx import get_and_save_uv_data
from CSV_uv_idx import process_uv_data_1
from CSV_uv_idx_final import process_uv_data_2
from API_sun import get_and_save_sun_data
from CSV_sun_cut import process_sun_data_1
from CSV_sun_interpolate import interpolate_sun_data
from CSV_merge import DataMerger
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import os

class EnsembleModel:
    def __init__(self, models):
        self.models = models

    def predict(self, X):
        predictions = [model.predict(X) for model in self.models]
        return np.mean(predictions, axis=0)

class WeatherData:
    def __init__(self, base_date, base_time, nx, ny, csv_file):
        self.base_date = base_date
        self.base_time = base_time
        self.nx = nx
        self.ny = ny
        self.csv_file = csv_file
class UVData:
    def __init__(self, base_date, base_time):
        self.base_date = base_date
        self.base_time = base_time

class SunDataRequest:
    def __init__(self, locdate, latitude, longitude, service_key):
        self.locdate = locdate
        self.latitude = latitude
        self.longitude = longitude
        self.service_key = service_key







def get_and_save_weather_data(weather_data):
    # API_weather 모듈의 get_weather_data와 save_to_csv 함수 호출
    header, data_rows = API_weather.get_weather_data(weather_data.base_date, weather_data.base_time, weather_data.nx, weather_data.ny)
    print(header)
    print(data_rows)
    if header is not None and data_rows is not None:
        API_weather.save_to_csv(header, data_rows, weather_data.csv_file)

    else:
        print('Failed to retrieve or save data.')

def main():
    current_datetime = datetime.now()
    date_input = current_datetime.strftime('%Y%m%d')
    date_input = input()
    input_date = datetime.strptime(date_input, "%Y%m%d")
    one_day_before = input_date - timedelta(days=1)
    input_date_str = input_date.strftime("%Y%m%d")
    one_day_before_str = one_day_before.strftime("%Y%m%d")

    # 날씨 데이터를 가져오기 위한 WeatherData 객체 생성
    ################## base_date='20231217'라면 12월 18일 00시부터 20일 23시까지의 데이터가 받아와짐 뒷부분 불필요한 데이터는 합칠때 자름 ############
    weather_data = WeatherData(base_date=one_day_before_str, base_time='0500', nx='45', ny='65', csv_file='weather_data_1.csv')

    # get_and_save_weather_data 함수 호출
    get_and_save_weather_data(weather_data)

    # process_weather_data1 함수 호출 (CSV_weather_cut1 모듈에서 가져옴)
    process_weather_data1(r'weather_data_1.csv', output_file_path='weather_data_2.csv')

    # process_weather_data2 함수 호출 (CSV_weather_cut2 모듈에서 가져옴)
    process_weather_data2(r'weather_data_2.csv', output_file_path='weather_data_3.csv')

    # UVData 객체 생성 ######### base_date='20231218'라면 12월 18일 00시부터 20일 23시까지의 데이터가 받아와짐 뒷부분 불필요한 데이터는 합칠때 자름 ############
    uv_data = UVData(base_date=input_date_str, base_time='00')
    get_and_save_uv_data(uv_data.base_date, uv_data.base_time)

    process_uv_data_1(input_file_path=r'D:\Advanced\API_CSV_pred\uv_data_raw.csv', output_file_path=r'uv_idx_3time.csv')

    process_uv_data_2(input_csv_path=r'uv_idx_3time.csv', output_csv_path=r'uv_idx_final.csv')

    # 파일 경로
    weather_data_path = r'weather_data_3.csv'
    uv_idx_path = r'uv_idx_final.csv'

    # 클래스 인스턴스 생성 및 메서드 호출
    for i in range(3):
        current_date = input_date + timedelta(days=i)
        current_date_str = current_date.strftime("%Y%m%d")

        # SunDataRequest 객체 생성 ####### locdate=current_date_str 라면 해당 날짜의 데이터만 뽑아준다 ###################
        sun_data_request = SunDataRequest(locdate=current_date_str, latitude='12607', longitude='3445',
                                          service_key='8gv6iLL5NMjLYTFifjbIh9yU4z/0xGYXgVgAJsYywpfYbMU1gCYAllIsVIrLEGM+DPi/NCXea0neY4fGRM2QmQ==')
        csv_file_path = fr'Sun_data_raw.csv'

        get_and_save_sun_data(sun_data_request.locdate, sun_data_request.latitude, sun_data_request.longitude,
                              csv_file_path)

        process_sun_data_1(input_csv_path=csv_file_path,
                           output_csv_path=fr'Sun_data_cut.csv')

        interpolate_sun_data(input_csv_path=fr'Sun_data_cut.csv',
                             output_csv_path=fr'Sun_data_interpolate.csv')


        sun_data_path = fr'Sun_data_interpolate.csv'
        output_path = fr'merged_data_{current_date_str}.csv'

        data_merger = DataMerger(weather_data_path, uv_idx_path, sun_data_path, output_path=output_path)

        # 메서드 호출
        data_merger.merge_data()

    # predict.py


    # ensemble_model.py

    import numpy as np
    input_date = pd.to_datetime(input_date)
    input_date = datetime.strptime(date_input, '%Y%m%d').strftime('%Y-%m-%d')

    for i in range(3):
        # input_date를 날짜로 변환
        input_date = pd.to_datetime(input_date)

        # input_date를 포맷에 맞게 문자열로 변환
        input_date_str = input_date.strftime('%Y%m%d')

        # 수정된 부분: 각 날짜에 대한 test_x를 불러올 때 현재 날짜를 사용
        test_x = pd.read_csv(f'merged_data_{input_date_str}.csv')
        # 데이터 불러오기
        train_x = pd.read_csv('train_x.csv')
        train_y = pd.read_csv('train_y.csv')


        # 'time' 열을 datetime 형식으로 변환
        train_x['time'] = pd.to_datetime(train_x['time'])
        train_y['time'] = pd.to_datetime(train_y['time'])
        test_x['time'] = pd.to_datetime(test_x['time'])

        # 'time' 열을 기준으로 두 데이터셋을 합침
        train_data = pd.merge(train_x, train_y, on='time', how='outer')

        # NaN 값은 0으로 채움
        train_data = train_data.fillna(0)

        # 특성과 레이블 분리
        X = train_data.drop(['time', 'amount'], axis=1)
        y = train_data['amount']

        # 입력된 날짜의 예측을 위한 데이터 전처리
        X_input_date = test_x[test_x['time'].dt.date == input_date.date()].drop(['time'], axis=1)
        X_input_date = X_input_date.fillna(0)

        # 앙상블 모델 불러오기
        loaded_ensemble_model = joblib.load('ensemble_model.joblib')

        # 불러온 앙상블 모델을 사용하여 예측
        ensemble_predictions = loaded_ensemble_model.predict(X_input_date)
        ensemble_predictions += 15
        ensemble_predictions[0:7] *= 0
        ensemble_predictions[15:17] *= 0.8
        ensemble_predictions[17:18] *= 0.5
        ensemble_predictions[21:] *= 0

        ensemble_predictions = ensemble_predictions * 162
        window_size = 1  # 이동 평균의 창 크기를 조절할 수 있습니다.
        ensemble_predictions = pd.Series(ensemble_predictions).rolling(window=window_size).mean()
        smoothed_predictions = pd.Series(ensemble_predictions).rolling(window=window_size).mean()

        selected_data = test_x[test_x['time'].dt.date == input_date.date()]

        # 'time' 열을 문자열에서 datetime.time으로 변환
        selected_data['time'] = pd.to_datetime(selected_data['time'], format='%H:%M:%S').dt.time

        # 모든 시간대를 포함하는 새로운 DataFrame을 생성합니다.
        all_time_values = pd.DataFrame({'time': pd.to_datetime(selected_data['time'], format='%H:%M:%S').dt.time})
        all_time_values['amount'] = 0.0

        # 'time'을 기준으로 두 데이터셋을 합칩니다.
        selected_data = pd.merge(all_time_values, selected_data, on='time', how='left')

        # NaN 값을 0으로 채웁니다.
        selected_data['amount'] = selected_data['amount'].fillna(0)

        # 'time'과 'amount' 열을 가지는 DataFrame을 생성합니다.
        output_df = pd.DataFrame({'time': selected_data['time'], 'amount': smoothed_predictions})

        # 수정된 부분: 현재 날짜를 이용하여 파일명 생성
        output_file_path = f'{input_date.date()}.csv'
        output_df.to_csv(output_file_path, index=False)
        output_df.to_csv(os.path.join("D:\Advanced\Data\predicted",f'{input_date.date()}.csv'), index=False)
        print(f'{input_date.date()}.csv 저장했습니다.')

        input_date = input_date + pd.DateOffset(days=1)

    input_date = input_date - pd.DateOffset(days=1)

    # 파일 경로 설정 (현재 폴더에 저장)
    output_folder = './'
    output_file_name = f'{input_date.date()}.csv'
    output_file_path = output_folder + output_file_name

    # CSV 파일 읽기
    Data = pd.read_csv(output_file_path)

    # 'time' 열의 날짜 부분 제거하고 시간 형식으로 변경
    Data['time'] = pd.to_datetime(Data['time']).dt.strftime('%H:%M:%S')

    # 'amount' 열을 float 형식으로 변경
    Data['amount'] = Data['amount'].astype(float)

    # 남은 시간에 해당하는 행 추가
    all_hours = pd.date_range("00:00", "23:00", freq="H").strftime('%H:%M:%S')
    existing_hours = Data['time'].unique()

    # 남은 시간 찾기
    remaining_hours = list(set(all_hours) - set(existing_hours))

    # 남은 시간에 해당하는 행 추가
    if remaining_hours:
        remaining_data = pd.DataFrame({'time': remaining_hours, 'amount': 0.0})
        Data = pd.concat([Data, remaining_data], ignore_index=True)

    # 시간순으로 정렬
    Data['time'] = pd.to_datetime(Data['time'])
    Data = Data.sort_values(by='time').reset_index(drop=True)

    # 'time' 열의 날짜 부분 제거하고 시간 형식으로 변경
    Data['time'] = pd.to_datetime(Data['time']).dt.strftime('%H:%M:%S')

    # 'amount' 열을 float 형식으로 변경
    Data['amount'] = Data['amount'].astype(float)


    # 수정된 DataFrame을 파일로 저장
    Data.to_csv(output_file_path, index=False)
    Data.to_csv(os.path.join("D:\Advanced\Data\predicted",output_file_name), index=False)

   



    current_directory = os.getcwd()

    # 폴더 내의 파일 목록 가져오기
    file_list = os.listdir(current_directory)

    # "merged_data_2023"로 시작하는 파일 삭제
    for file_name in file_list:
        if file_name.startswith("merged_data_2023"):
            file_path = os.path.join(current_directory, file_name)
            os.remove(file_path)
            print(f"{file_name} deleted.")





# main 함수 호출
if __name__ == "__main__":


    main()