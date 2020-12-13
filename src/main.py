import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup


def write_json(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)


def get_html(road_number):
    url = 'https://roads.dot.ca.gov/'
    headers = {
        'Host': 'roads.dot.ca.gov',
        'Referer': 'https://roads.dot.ca.gov/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    }
    response = requests.post(url, data={'roadnumber': road_number, 'submit': 'Search'}, headers=headers)
    return response.text


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('main', attrs={'class': 'main-primary'})
    cities = div.find_all('strong')
    data = []
    for city in cities:
        current_city = city.text.strip().replace('[', '').replace(']', '')
        current_city_status = str(city.next_sibling.next_sibling).strip()
        data.append(
            {
                'city': current_city,
                'status': current_city_status,
                'date': datetime.now().strftime('%Y-%m-%d, %H:%M')
            }
        )
    return data


def main():
    html = get_html(80)
    write_json(get_page_data(html))


if __name__ == '__main__':
    main()
