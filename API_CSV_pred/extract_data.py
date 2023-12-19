import pandas as pd
from bs4 import BeautifulSoup

def extract_data_from_html(html_file_path):
    # HTML 파일을 읽기 모드로 열고 Beautiful Soup를 사용하여 파싱합니다.
    with open(html_file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # 데이터를 담을 빈 리스트를 만듭니다.
    data = []

    # 표 내의 모든 행(tr)을 찾습니다.
    for row in soup.find_all("tr"):
        # 각 행에서 셀(td)을 찾습니다.
        cells = row.find_all("td")
        if cells:
            # 셀 내의 텍스트를 추출하여 리스트에 추가합니다.
            row_data = [cell.get_text(strip=True) for cell in cells]

            # 숫자 형식의 데이터는 숫자로 변환합니다.
            for i in range(2, len(row_data)):
                try:
                    row_data[i] = int(row_data[i])
                except ValueError:
                    pass  # 숫자로 변환할 수 없는 경우 그대로 둡니다.

            data.append(row_data)

    # 데이터를 Pandas 데이터프레임으로 변환합니다.
    df = pd.DataFrame(data, columns=["발전소명", "시간", "PV 발전량", "ESS 충전량", "ESS 방전량"])

    row_count = df.shape[0]-1
    # 마지막 행의 데이터를 저장
    last_row_1 = df.iloc[row_count, df.columns.get_loc("발전소명")]
    last_row_2 = df.iloc[row_count, df.columns.get_loc('시간')]
    last_row_3 = df.iloc[row_count, df.columns.get_loc('PV 발전량')]
    last_row_4 = df.iloc[row_count, df.columns.get_loc('ESS 충전량')]
    df.at[row_count, '발전소명'] = ' '
    df.at[row_count, '시간'] = last_row_1
    df.at[row_count, 'PV 발전량'] = int(last_row_2)
    df.at[row_count, 'ESS 충전량'] = last_row_3
    df.at[row_count, 'ESS 방전량'] = last_row_4



    return df





# 함수를 호출하여 데이터프레임을 생성합니다.
if __name__ == '__main__':
    # HTML 파일 경로를 지정하고 데이터를 추출합니다.
    html_file_path = "D:\Advanced\Crawl\Download\TimeData_2023-09-07.html"
    df = extract_data_from_html(html_file_path)

    # 결과를 출력합니다.
    print(df)