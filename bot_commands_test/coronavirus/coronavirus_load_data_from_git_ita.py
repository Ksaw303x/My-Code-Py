import csv
from io import StringIO
from datetime import datetime
import requests
import re
from pprint import pprint
from pvlv_database import SharedDatabase


class Scrapper(object):

    def __init__(self):
        self.__data = {}

    def __web_scrapper(self):

        timestamp = datetime.utcnow()

        file_url = 'pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni'
        ts = timestamp.strftime('%Y%m%d')
        url = 'https://raw.githubusercontent.com/{}-{}.csv'.format(
            file_url,
            ts,
        )

        res = requests.get(url)
        # check the status code, if is not 200 it means that the file do not exist
        if res.status_code > 200:
            raise FileNotFoundError
        file = StringIO(res.content.decode('utf-8'))  # create the buffer file
        csv_file = csv.reader(file, delimiter=',')

        for row_counter, row in enumerate(csv_file):
            if row_counter > 0:
                key = ''.join(re.findall('[a-zA-Z]+', row[3].lower()))
                self.__data[key] = {
                    'rank': row_counter,
                    'cases': int(row[14]) if row[14] != '' else 0,
                    'new_cases': int(row[14]) if row[14] != '' else 0,
                    'deaths': int(row[13]) if row[13] != '' else 0,
                    'new_deaths': row[4],
                    'recovered': int(row[12]) if row[12] != '' else 0,
                    'critical_cases': row[7],
                }

    @property
    def download_data(self):
        self.__web_scrapper()
        return self.__data


class Data:

    def __init__(self):

        self.sdb = SharedDatabase()
        self.data_object = DataObject(self.sdb.get_data('coronavirus', 0))

    def update_data(self):
        dg_it = DataGrinderItaly()
        dg = DataGrinder()
        data_now_it = dg_it.download_data
        data_now = dg.download_data

        data_now.update(data_now_it)

        if self.data_object.data:
            """
            If the last element in the array contain already data of today
            Then update that data
            """
            if datetime.today().day == self.data_object.data[-1]['date'].day:
                self.data_object.data[-1]['date'] = datetime.utcnow()
                self.data_object.data[-1]['countries'] = data_now
                self.sdb.set_data('coronavirus', 0, self.data_object.build_data())  # save the data
                return

        # Else Create a new array element (case1 no data, case2 new day)
        self.data_object.data.append({
            'date': datetime.utcnow(),
            'countries': data_now,
        })
        self.sdb.set_data('coronavirus', 0, self.data_object.build_data())  # save the data




def main(self):
    data = self.download_data
    pprint(data)




if __name__ == '__main__':
    i = Scrapper()
    i.main()
