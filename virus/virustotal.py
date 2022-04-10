import base64
import json
import requests

API_KEY = '00c4e361d81446bf1830ece5bf8052df1cca62c718a471ea932a552cb0b310ae'
BASE_API_URL = 'https://www.virustotal.com/api/v3'
HEADERS = {'x-apikey': API_KEY}


def get_ip_data(ip: str):
    res = requests.get(f'{BASE_API_URL}/ip_addresses/{ip}', headers=HEADERS)

    json_response = json.loads(res.content)

    from pprint import pprint
    pprint(json_response['data']['attributes']['last_analysis_stats'])


def get_url_data(url: str):

    encoded_url = base64.urlsafe_b64encode(url.encode()).decode().strip("=")

    res = requests.get(f'{BASE_API_URL}/urls/{encoded_url}', headers=HEADERS)

    json_response = json.loads(res.content)

    from pprint import pprint
    pprint(json_response['data']['attributes']['last_analysis_stats'])


if __name__ == '__main__':
    get_url_data('https://www.virustotal.com/api/v3')
    get_ip_data('1.1.1.1')
