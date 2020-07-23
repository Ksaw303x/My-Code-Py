import csv
from io import StringIO
from datetime import datetime, timedelta
from pprint import pprint
import requests
from pvlv_database import DataCommands


class Scrapper(object):

    def __init__(self):

        self.db = DataCommands()
        self.data = self.db.get_command_data('coronavirus')

    @staticmethod
    def __data_conversion(timestamp):
        try:
            return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')
        except:
            pass
        try:
            return datetime.strptime(timestamp, '%m/%d/%y %H:%M')
        except:
            pass
        try:
            return datetime.strptime(timestamp, '%m/%d/%Y %H:%M')
        except:
            pass

    def web_scrapper(self, url):

        res = requests.get(url)
        # check the status code, if is not 200 it means that the file do not exist
        if res.status_code > 200:
            return False
        file = StringIO(res.content.decode('utf-8'))  # create the buffer file
        csv_file = csv.reader(file, delimiter=',')

        row_counter = 0
        for row in csv_file:

            if row_counter > 0:

                region = row[0]
                county = row[1].lower()
                timestamp = self.__data_conversion(row[2]).strftime('%Y-%m-%dT%H:%M:%S')
                confirmed = int(row[3]) if row[3] != '' else 0
                deaths = int(row[4]) if row[4] != '' else 0
                recovered = int(row[5]) if row[5] != '' else 0

                try:
                    self.data[county][timestamp] = {
                        'region': region,
                        'cases': confirmed,
                        'recovered': recovered,
                        'deaths': deaths,
                    }
                except KeyError:
                    self.data[county] = {
                        timestamp: {
                            'region': region,
                            'cases': confirmed,
                            'recovered': recovered,
                            'deaths': deaths,
                        }
                    }

            row_counter += 1
        return True

    def main(self):

        file_url = 'CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports'
        #file_url = 'CSSEGISandData/COVID-19/master/archived_data/test'

        # Day 0 22-01-2020
        timestamp = datetime.strptime('28-01-2020', '%d-%m-%Y')
        now = datetime.utcnow()

        while timestamp < now:

            ts = timestamp.strftime('%m-%d-%Y')
            url = 'https://raw.githubusercontent.com/{}/{}.csv'.format(
                file_url,
                ts,
            )
            success = self.web_scrapper(url)
            if success:
                print('{} success'.format(ts+'.csv'))
            else:
                print('{} not found'.format(ts+'.csv'))

            timestamp += timedelta(days=1)

        self.db.set_command_data('coronavirus', self.data)
        print('Job Done')


if __name__ == '__main__':
    i = Scrapper()
    i.main()
