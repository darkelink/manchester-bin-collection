#!/bin/python

from datetime import datetime
import sys

from bs4 import BeautifulSoup
import requests


UPRN = ''


class BinRequest:
    url = 'https://cms.manchester.gov.uk/bincollections'
    data = {
        'mcc_bin_dates_submit': 'Go',
    }

    def __init__(self, uprn, *args, **kwargs):
        self.data['mcc_bin_dates_uprn'] = uprn

    def get_raw_data(self):
        response = requests.post(self.url, data=self.data)
        if response.status_code != 200:
            raise Exception()
        return response.text

    def parse_response(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        result = {}
        for collection in soup.find_all(class_='collection'):
            title = collection.find('h3').findAll(text=True)
            caption = collection.find('p').text

            bin = title[0].strip()[:-4]
            date = caption.strip()[16:]
            date = datetime.strptime(date, '%A %d %b %Y').date()
            result[bin] = date

        return result

    def get_bin_dates(self):
        raw_data = self.get_raw_data()
        return self.parse_response(raw_data)


def main(*args, **kwargs):
    bins = BinRequest(UPRN).get_bin_dates()
    for bin, date in bins.items():
        print('{0:15s} - {1:s}'.format(bin, date.isoformat()))
    return 0

if __name__ == '__main__':
    exit(main(sys.argv[1:]))
