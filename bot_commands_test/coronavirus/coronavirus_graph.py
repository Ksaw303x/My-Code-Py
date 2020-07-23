from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from pvlv_database import DataCommands


class CoronavirusGraphBuilder(object):

    def __init__(self):

        self.db = DataCommands()
        self.db_data = self.db.get_command_data('coronavirus')

    @staticmethod
    def __timestamp_conversion(timestamp):
        return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')

    def __merge_data(self, data):

        data_merge = {}
        current_day = None
        current_day_timestamp = None
        for day in data:
            day_timestamp = self.__timestamp_conversion(day)

            cases = data[day].get('cases')
            recovered = data[day].get('recovered')
            deaths = data[day].get('deaths')

            if not current_day:
                current_day = day
                current_day_timestamp = day_timestamp

            if not day_timestamp.day == current_day_timestamp.day:
                current_day = day
                current_day_timestamp = day_timestamp

            d = data_merge.get('current_day')
            if d:
                data_merge[current_day]['cases'] += cases
                data_merge[current_day]['recovered'] += recovered
                data_merge[current_day]['deaths'] += deaths
            else:
                data_merge[current_day] = {}
                data_merge[current_day]['cases'] = cases
                data_merge[current_day]['recovered'] = recovered
                data_merge[current_day]['deaths'] = deaths

        return data_merge

    def __format_data(self, country):
        try:
            data = self.db_data[country]

            formatted_data = [[], [], []]

            timestamps = list(data.keys())

            prev_timestamp = timestamps.pop(0)
            first_timestamp = self.__timestamp_conversion(prev_timestamp)
            timestamp_cursor = first_timestamp

            for timestamp_str in timestamps:

                while timestamp_cursor < self.__timestamp_conversion(timestamp_str):

                    timestamp_cursor += timedelta(days=1)
                    formatted_data[0].append(int(data[prev_timestamp].get('cases')))
                    formatted_data[1].append(int(data[prev_timestamp].get('deaths')))
                    formatted_data[2].append(int(data[prev_timestamp].get('recovered')))

                prev_timestamp = timestamp_str

            # load the last timestamp data
            formatted_data[0].append(int(data[timestamps[-1]].get('cases')))
            formatted_data[1].append(int(data[timestamps[-1]].get('deaths')))
            formatted_data[2].append(int(data[timestamps[-1]].get('recovered')))

            # return: [start - end], formatted data
            start = first_timestamp.strftime('%d-%m-%Y')
            stop = self.__timestamp_conversion(timestamps[-1]).strftime('%d-%m-%Y')
            return [start, stop], formatted_data

        except Exception as exc:
            print(exc)
            return '', []

    def plot(self, country):

        data_range, formatted_data = self.__format_data(country)

        fig, ax = plt.subplots()
        ax.plot(formatted_data[0], '.-', color='#aa0504', alpha=0.7, label='Infected')
        ax.plot(formatted_data[1], '.-', color='#110000', alpha=0.7, label='Deaths')
        ax.plot(formatted_data[2], '.-', color='#087800', alpha=0.7, label='Recovered')
        plt.grid(axis='y', alpha=0.75)

        legend = ax.legend(loc='upper center', shadow=True, fontsize='x-large')
        legend.get_frame()

        plt.title('Number of Infected People in {}'.format(country))
        plt.ylabel('Infected / Death / Recovered value'.format(country))
        plt.xlabel('Day Zero: {} - Last update: {}'.format(data_range[0], data_range[1]))
        plt.savefig('plots_out/{}.png'.format(country))
        plt.show()


if __name__ == '__main__':
    i = CoronavirusGraphBuilder()
    # country, region; if the regions are specified in the data. Else leave blank
    i.plot('italy')
