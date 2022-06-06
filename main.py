from functools import lru_cache

import requests
from bs4 import BeautifulSoup
import config as cfg
import logging

import util

logging.basicConfig(
    level=logging.DEBUG,
    filename="mylog.log",
    format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt='%H:%M:%S',
)


def get_data(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0'}
    req = requests.get(url, headers)
    # logging.info(f'raw data from page :  {req.text}')
    return req


@lru_cache(maxsize=500)
def save_data_to_html(url: str, file_name: str):
    req = get_data(url)
    with open(f'html/{file_name}', 'w') as file:
        file.write(req.text)
    return file_name


# save_data_to_html('https://br.fas.gov.ru/', 'project.html')

def get_list_of_refs(html_file_name: str):
    with open('html/' + html_file_name) as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')
    rows = soup.find('div', class_='container-fluid').find_all('div', class_='col-sm-10')

    # get list of hrefs
    project_urls = []
    for row in rows:
        project_url = cfg.url + row.find('a', target='_blank').get('href')
        project_urls.append(project_url)

    for project_url in project_urls[3:4]:
        req = get_data(project_url)  # get_data() return req = request.get(url, list_of_headers)
        project_name = project_url.split('/')[4]
        # print(f'project URL : {project_url}')

        with open(f'data/{project_name}.html', 'w') as file:
            file.write(req.text)

        with open(f'data/{project_name}.html') as file:
            src_s = file.read()

        soup_s = BeautifulSoup(src_s, 'lxml')
        project_data = soup_s.find('div', class_='container-fluid')
        # get project name
        project_name = project_data.find_all('h3')[0].text
        # print(f'project name : {project_name}')

        # get all list_of_headers after project name : tag <a> in class_='container-fluid'
        list_of_headers = project_data.find_all('a')
        print(f'tyoe of list of headers : {type(list_of_headers)}')
        print(list_of_headers)
        # headers list
        keys = ['procedure', 'start_date', 'divisions', 'market_type', 'case_state']
        #TODO найти совпадения по ключевым словам keys
        # если есть совпадение нужно взять этот элемент объекта soup из list_of_headers[i] и извлечь из него .text

        # print(f'procedure value : \n'
        #       f'{list(filter(lambda list_item: "procedure" in list_item, str(list_of_headers).split(",")))}')

        util.list_filter(keys, list_of_headers)

        headers = []
        for key in keys:
            for i in range(len(list_of_headers)):
                if filter(lambda a: key in a, str(list_of_headers).split(',')):
                    headers.append(list_of_headers[i])
        # print(headers)

        try:
            procedure = list_of_headers[0].text
        except Exception as e:
            procedure = None
            print('There is not field: DIVISION; '
                  '\ntype of exception: %s;'
                  '\nexception: %s;'
                  '\nfields value changed to %s', type(e), e, type(procedure))
        try:
            start_date = list_of_headers[1].text
        except Exception as e:
            start_date = None
            print('There is not field: DIVISION; '
                  '\ntype of exception: %s;'
                  '\nexception: %s;'
                  '\nfields value changed to %s', type(e), e, type(start_date))
        try:
            divisions = list_of_headers[2].text
        except Exception as e:
            divisions = None
            print('There is not field: DIVISION; '
                  '\ntype of exception: %s;'
                  '\nexception: %s;'
                  '\nfields value changed to %s', type(e), e, type(divisions))
        try:
            market_type = list_of_headers[3].text
        except Exception as e:
            market_type = 'has no market type'
            print('There is not field: DIVISION; '
                  '\ntype of exception: %s;'
                  '\nexception: %s;'
                  '\nfields value changed to %s', type(e), e, type(market_type))
        try:
            case_state = list_of_headers[4].text
        except Exception as e:
            case_state = 'has no case_state'
            print('There is not field: DIVISION; '
                  '\ntype of exception: %s;'
                  '\nexception: %s;'
                  '\nfields value changed to %s', type(e), e, type(case_state))

        print(f'procedure name : {list_of_headers}')
        print(f' procedure : {procedure}\n '
              f'start_date : {start_date}\n '
              f'divisions : {divisions}\n '
              f'market_type : {market_type}\n '
              f'case_state : {case_state}')
        # get


get_list_of_refs('project.html')
