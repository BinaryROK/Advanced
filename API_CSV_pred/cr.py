import pandas as pd
import numpy as np
import os
import time
import psutil
from datetime import datetime as dt  # 이름을 바꿈
import subprocess

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import extract_data as extract

pd.set_option('display.Width', 5000)
pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 5000)

DownloadPath = r"D:\Advanced\Data\zaraData"
HYOSUNG = 'http://hess.hyosung.com/HsMain/HM020.aspx'


def driversetting(DownloadPath):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {"download.default_directory": DownloadPath,
                                              "download.prompt_for_download": False,
                                              "download.directory_upgrade": True,
                                              "safebrowsing_for_trusted_source_enabled": False,
                                              "safebrowsing.enabled": False})

    # options.add_argument("headless") # 켜두면 크롬창이 뜨지않고 실행됨
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shn-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(3)

    return driver


def gen(TargetDay, Farm):  # TargetDay, Farm, Method
    driver = driversetting(DownloadPath)

    driver.get(HYOSUNG)
    print('run website')
    time.sleep(3)

    driver.find_element(By.XPATH, '//*[@id="Txt_1"]').send_keys('jarasolar')
    driver.find_element(By.XPATH, '//*[@id="Txt_2"]').send_keys('abcd1234')
    driver.find_element(By.XPATH, '//*[@id="imageField"]').click()

    print('login')
    time.sleep(3)

    # 팝업닫기
    driver.find_element(By.XPATH, '//*[@id="popupContainer"]/div/div/div/div[2]/button[1]').click()

    driver.find_element(By.XPATH, '//*[@id="form1"]/div[4]/div[1]/div/ul[2]/a[5]/li').click()
    print('Satistical Report')
    time.sleep(3)

    # 16MW
    driver.find_element(By.XPATH, '//*[@id="SrTop_cbo_plant"]/option[' + str(Farm) + ']').click()
    print('Select Farm')
    time.sleep(3)

    # Date Clear
    driver.find_element(By.XPATH, '//*[@id="txt_Calendar"]').clear()
    # time.sleep(pa.waitseconds)

    # Date Input
    driver.find_element(By.XPATH, '//*[@id="txt_Calendar"]').send_keys(TargetDay)
    print('Put new date')
    time.sleep(3)

    # Close the calender
    driver.find_element(By.XPATH, '//*[@id="txt_Calendar"]').send_keys(Keys.ENTER)
    print('Close the calender')
    time.sleep(3)

    # Search
    driver.find_element(By.XPATH, '//*[@id="submitbtn"]').click()
    print('Search')
    time.sleep(3)

    # Download
    driver.find_element(By.XPATH, '//*[@id="exldownbtn"]').click()
    print('Download')
    time.sleep(3)

    driver.quit()  # 웹 드라이버 종료
    time.sleep(3)  # 명시적인 대기 시간 추가

    for process in psutil.process_iter():
        if "chromedriver" in process.name().lower():
            process.kill()  # ChromeDriver 프로세스 종료

    # 다운로드한 파일명 바꾸기 html로
    print("rename file")
    today_date_str = dt.now().strftime("%Y-%m-%d")
    downloaded_filename = "TimeData_" + today_date_str + ".xls"
    downloaded_file_path = os.path.join(DownloadPath, downloaded_filename)  # 다운로드한 파일 경로 및 이름
    new_file_name = os.path.join(DownloadPath, "TimeData_" + TargetDay + ".html")  # 새 파일 이름 및 경로
    os.rename(downloaded_file_path, new_file_name)

    print("filename changed")
    # html에서 데이터 뽑아서 데이터프레임 만들기
    # Extract data from HTML and select necessary columns
    Data = extract.extract_data_from_html(os.path.join(DownloadPath, new_file_name))
    Data = Data[["시간", "PV 발전량"]]

    new_column_names = {'시간': 'time', 'PV 발전량': 'amount'}
    Data.rename(columns=new_column_names, inplace=True)

    # 마지막 행이 'Sum'인 경우 삭제
    if Data.iloc[-1]['time'] == 'Sum':
        Data = Data[:-1]

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
    Data = Data.sort_values(by='time')
    
    # Save data to CSV (overwrite if file already exists)
    csv_filename = os.path.join(DownloadPath, TargetDay + ".csv")
    Data.to_csv(csv_filename, index=False)
    print("Data saved to CSV")

    # Delete the file after use
    if os.path.exists(new_file_name):
        os.remove(new_file_name)
        print("File deleted")
    else:
        print("File does not exist")

    return Data


if __name__ == '__main__':
    Farm = 1

    # 현재 날짜를 'YYYY-MM-DD' 형식의 문자열로 가져오기
    today_date_str = dt.today().strftime('%Y-%m-%d')

    # farm과 TargetDay 설정
    farm = 1
    TargetDay = today_date_str

    # gen 함수 호출
    gen(TargetDay, farm)

    # Git 저장소 경로
    #repo_path = "C:\\Advanced\\Advanced"

    # 변경사항을 스테이징 영역에 추가
    #subprocess.run(["git", "add", "Data"], cwd=repo_path)

    # 변경 내용 커밋
    #commit_message = "Add ZaraData" + dt.now().strftime("%Y-%m-%d %H:%M:%S")
    #subprocess.run(["git", "commit", "-m", commit_message], cwd=repo_path)

    # 변경 내용 푸시
    #subprocess.run(["git", "push", "origin", "main"], cwd=repo_path)