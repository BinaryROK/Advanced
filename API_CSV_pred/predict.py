# predict.py

import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
# ensemble_model.py

import numpy as np

class EnsembleModel:
    def __init__(self, models):
        self.models = models

    def predict(self, X):
        predictions = [model.predict(X) for model in self.models]
        return np.mean(predictions, axis=0)

# 데이터 불러오기
train_x = pd.read_csv('train_x.csv')
train_y = pd.read_csv('train_y.csv')
test_x = pd.read_csv('merged_data_20231220.csv')

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


# 앙상블 모델 불러오기
loaded_ensemble_model = joblib.load('ensemble_model.joblib')

# 사용자로부터 날짜 입력 받기
input_date = input("날짜를 입력하세요 (예: '2022-06-20'): ")
input_date = pd.to_datetime(input_date)

# 입력된 날짜의 예측을 위한 데이터 전처리
X_input_date = test_x[test_x['time'].dt.date == input_date.date()].drop(['time'], axis=1)
X_input_date = X_input_date.fillna(0)

# 불러온 앙상블 모델을 사용하여 예측

ensemble_predictions = loaded_ensemble_model.predict(X_input_date)
ensemble_predictions += 15
ensemble_predictions[0:7] *= 0
ensemble_predictions[17:20] *= 0.3
ensemble_predictions[21:] *= 0

ensemble_predictions = ensemble_predictions * 162 *2
smoothed_predictions = pd.Series(ensemble_predictions).rolling(window=3, min_periods=1).mean().values

# 예측 결과 시각화
plt.figure(figsize=(12, 6))
plt.plot(test_x[test_x['time'].dt.date == input_date.date()]['time'], ensemble_predictions, label='Ensemble', marker='o')
#plt.plot(train_y[train_y['time'].dt.date == input_date.date()]['time'], train_y[train_y['time'].dt.date == input_date.date()]['amount'], label='Actual', marker='x')

plt.title(f'{input_date.date()} Ensemble Predictions')
plt.xlabel('Time')
plt.ylabel('Amount')
plt.legend()
plt.show()