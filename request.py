import requests
import logging
from lxml import html
import pandas as pd
from io import BytesIO

logging.basicConfig(level=logging.DEBUG)  # Устанавливаем уровень логирования
logger = logging.getLogger(__name__)      # Получаем логгер для текущего модуля

proxies = {
    "http": "http://51.79.71.106:8080",
}


# Ссылка на сайт с расписанием ВМК
URL = "https://kpfu.ru/computing-technology/raspisanie" 

# xpath на расписание
Xpath_to_link_with_schedule = '//*[@id="ss_content"]/div[2]/div/div[2]/div[1]/div/div[2]/div/p[2]/strong/a'


def get_response(URL):
    response = requests.get(URL,proxies=proxies)
    logger.info(f"Получены данные:  option={response.status_code}")
    return response

def find_link(response):
    tree = html.fromstring(response.content)
    link_content = tree.xpath(Xpath_to_link_with_schedule)
    link = link_content[0].get('href')    
    return link
def get_data(link):
    response = requests.get(link)
    excel_file = BytesIO(response.content)
    return excel_file

def main():
    response = get_response(URL)
    link = find_link(response)    
    data = get_data(link)
    return data
if __name__ == ("__main__"):
    data = main()    
    print(data)

