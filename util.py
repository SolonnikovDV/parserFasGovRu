import logging
import socket

import requests
from bs4 import BeautifulSoup, ResultSet

logging.basicConfig(level=logging.DEBUG,
                    filename="mylog.log",
                    format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
                    datefmt='%H:%M:%S'
                    )

# array chars to replace rep = [",", " ", "  ", "-", "'", "/".........]
def replace(rep: [], complaint_name: str):
    for item in rep:
        if item in complaint_name:
            complaint_name = complaint_name.replace(item, "_")
    # logging.debug(f'complaint name replace func: {complaint_name}')
    return complaint_name

def filter_list(keys: [], list_items):
    for key in keys:
        filtered_object = filter(lambda item: key in item, str(list_items).split(","))
        if filtered_object is not None:
            print(list(filtered_object))

def list_filter(keys: [], list_items: ResultSet):
    items = str(list_items).split(',')
    mach_indexes = []
    sort_list = ResultSet
    for key in keys:
        for i in range(len(items) - 1):
            if key in items[i]:
                mach_indexes.append(i)
    for i in mach_indexes:
        ind = int(mach_indexes[i])
        print(list_items[ind])
        # sort_list.append(list_items[ind])


def get_request(url: str, headers: []):
    req = requests.get(url=url, headers=headers)
    src = req.text
    return src

def check_internet_connection():
    REMOTE_SERVER = "www.google.com"

    def is_connected(hostname):
        try:
            # see if we can resolve the host name -- tells us if there is
            # a DNS listening
            host = socket.gethostbyname(hostname)
            # connect to the host -- tells us if the host is actually
            # reachable
            s = socket.create_connection((host, 80), 2)
            return True
        except:
            pass
        return False

def split_str():
    str = 'https://br.fas.gov.ru/cases/271b7ff6-23ae-46d9-bffc-18d4c1caecef'
    new_str = str.split('/')[4]
    return new_str

if __name__ == '__main__':
    print(split_str())

    # logging.debug(f'split {split_str()}')