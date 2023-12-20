from urllib.request import Request, urlopen
from urllib.parse import urlencode
import csv
import json

def get_and_save_uv_data(base_date, base_time):
    # Build UV parameter dictionary
    uv_params = {
        'serviceKey': '8gv6iLL5NMjLYTFifjbIh9yU4z/0xGYXgVgAJsYywpfYbMU1gCYAllIsVIrLEGM+DPi/NCXea0neY4fGRM2QmQ==',
        'areaNo': '4691040000', # 전라남도 신안군 안좌면
        'time': f'{base_date}{base_time}',
        'dataType': 'JSON'
    }

    # Build URL with parameters
    uv_url = 'http://apis.data.go.kr/1360000/LivingWthrIdxServiceV4/getUVIdxV4?' + urlencode(uv_params)

    try:
        # Make the request
        uv_request = Request(uv_url)
        uv_request.get_method = lambda: 'GET'
        uv_response_body = urlopen(uv_request).read()

        # Parse JSON response
        uv_data = json.loads(uv_response_body)

        # Check if the response contains data
        if 'response' in uv_data and 'body' in uv_data['response'] and 'items' in uv_data['response']['body']:
            uv_items = uv_data['response']['body']['items']['item']

            # Check if items is not empty
            if uv_items:
                # Extract time and corresponding values
                time_values = {f"h{i}": item[f"h{i}"] for item in uv_items for i in range(0, 76, 3)}

                # Specify the CSV file name
                csv_file = r'D:\Advanced\API_CSV_pred\uv_data_raw.csv'

                # Define the order of columns for the CSV file
                header = ['time'] + [f"h{i}" for i in range(0, 76, 3)]

                # Write the data to a CSV file with utf-8-sig encoding
                with open(csv_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
                    # Create a CSV writer object
                    csv_writer = csv.writer(csvfile)

                    # Write the header row
                    csv_writer.writerow(header)

                    # Write the data rows
                    data_row = [uv_params['time']] + [time_values[column] for column in header[1:]]
                    csv_writer.writerow(data_row)

                print(f'Data successfully saved to {csv_file}')
            else:
                print('No data available.')
        else:
            print('Invalid response format.')
    except Exception as e:
        print(f'Error during request: {e}')


