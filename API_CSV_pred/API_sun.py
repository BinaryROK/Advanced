import requests
import xmltodict
import csv

def get_and_save_sun_data(locdate, latitude, longitude, csv_file_path):
    url = 'http://apis.data.go.kr/B090041/openapi/service/SrAltudeInfoService/getLCSrAltudeInfo'

    uv_params = {
        'serviceKey': '8gv6iLL5NMjLYTFifjbIh9yU4z/0xGYXgVgAJsYywpfYbMU1gCYAllIsVIrLEGM+DPi/NCXea0neY4fGRM2QmQ==',
        'locdate': locdate,
        'latitude': latitude,
        'longitude': longitude,
        'dnYn': 'Y',
        'totalCount': '1'
    }

    response = requests.get(url, params=uv_params)

    # Parse XML to dictionary
    data_dict = xmltodict.parse(response.content)

    # Extract relevant data
    altitude_data = data_dict['response']['body']['items']['item']

    # Extract only the needed columns
    selected_columns = {
        'locdate': altitude_data['locdate'],
        'azimuth_09': altitude_data['azimuth_09'],
        'altitude_09': altitude_data['altitude_09'],
        'azimuth_12': altitude_data['azimuth_12'],
        'altitude_12': altitude_data['altitude_12'],
        'azimuth_15': altitude_data['azimuth_15'],
        'altitude_15': altitude_data['altitude_15'],
        'azimuth_18': altitude_data['azimuth_18'],
        'altitude_18': altitude_data['altitude_18'],
    }

    # Write to CSV with UTF-8 encoding
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=selected_columns.keys())
        writer.writeheader()
        writer.writerow(selected_columns)

    print(f'Data has been written to {csv_file_path}')


