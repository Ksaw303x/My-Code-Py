import csv
from io import StringIO
from datetime import datetime, timedelta
from pprint import pprint
import requests
from pvlv_database import DataCommands


class MigrateDb(object):

    def __init__(self):

        self.db = DataCommands()
        self.data = self.db.get_command_data('coronavirus')

    @staticmethod
    def __timestamp_conversion(timestamp):
        return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')

    def main(self):

        country = self.data.get('italy')


        del self.data['italy']
        pprint(country)
        self.data['italy2'] = country
        self.db.set_command_data('coronavirus', self.data)
        input()
        # --------------------
        timestamps = list(country.keys())

        new_data_country = {}

        prev_timestamp = timestamps.pop(0)
        prev_data = country[prev_timestamp]

        timestamp_cursor = self.__timestamp_conversion(prev_timestamp)

        for timestamp_str in timestamps:

            while timestamp_cursor < self.__timestamp_conversion(timestamp_str):

                timestamp_cursor += timedelta(days=1)
                new_data_country[timestamp_cursor.strftime('%Y-%m-%dT%H:%M:%S')] = prev_data

            timestamp_cursor = self.__timestamp_conversion(timestamp_str)
            prev_timestamp = timestamp_str
            prev_data = country[timestamp_str]

        # load the last timestamp data

        new_data_country[timestamp_cursor.strftime('%Y-%m-%dT%H:%M:%S')] = country[timestamps[-1]]

        self.data['italy'] = new_data_country

        pprint(new_data_country)
        # self.db.set_command_data('coronavirus', self.data)
        print('done')


if __name__ == '__main__':
    i = MigrateDb()
    i.main()
