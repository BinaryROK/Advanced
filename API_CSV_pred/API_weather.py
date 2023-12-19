import requests
import csv
import json

def get_weather_data(base_date, base_time, nx, ny):
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'

    params = {
        'serviceKey': '8gv6iLL5NMjLYTFifjbIh9yU4z/0xGYXgVgAJsYywpfYbMU1gCYAllIsVIrLEGM+DPi/NCXea0neY4fGRM2QmQ==',
        'pageNo': '1',
        'numOfRows': '1000',
        'dataType': 'JSON',
        'base_date': base_date,
        'base_time': base_time,
        'nx': nx,
        'ny': ny
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        json_data = response.json()
        items = json_data.get('response', {}).get('body', {}).get('items', {}).get('item', [])

        if items:
            unwanted_categories = ['POP', 'PTY', 'PRY', 'SKY', 'TMN', 'TMX', 'UUU', 'VVV', 'WAV']
            filtered_items = [item for item in items if item['category'] not in unwanted_categories]

            if filtered_items:
                header = [key for key in filtered_items[0].keys() if key not in ['baseDate', 'baseTime', 'nx', 'ny']]
                data_rows = [[value for key, value in item.items() if key not in ['baseDate', 'baseTime', 'nx', 'ny']] for item in filtered_items]

                return header, data_rows
            else:
                return None, None  # No data after filtering
        else:
            return None, None  # Response does not contain the expected data structure
    else:
        return None, None  # Request failed with status code

def save_to_csv(header, data_rows, csv_file):
    with open(csv_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(header)
        csv_writer.writerows(data_rows)

    print(f'Data successfully saved to {csv_file}')


