import json
from datetime import datetime
from pprint import pprint
import requests
from bs4 import BeautifulSoup


class Scrapper(object):

    def __init__(self):

        """
        self.bot = bot
        self.language = language
        self.command = command
        """
        self.arg = ''

        """
        self._sort = None
        _vars = ['_sort']
        for param in params:
            name = '_{}'.format(param[0])
            setattr(self, name, param[1])
        """

        # Counters for total data
        self.total_cases = 0
        self.total_new_cases = 0
        self.total_deaths = 0
        self.total_new_deaths = 0
        self.total_recovered = 0
        self.total_critical_cases = 0

        self.data = {}

    def __add_data(self, data, rank):

        if len(data) < 8:
            return

        county = data[0].lower()
        date = datetime.utcnow()
        cases = data[1]
        new_cases = data[2]
        deaths = data[3]
        new_deaths = data[4]
        recovered = data[5]
        critical_cases = data[6]
        continent = data[7]

        self.data[county] = {
            'rank': rank,
            'date': date,
            'cases': cases,
            'new_cases': new_cases,
            'deaths': deaths,
            'new_deaths': new_deaths,
            'recovered': recovered,
            'critical_cases': critical_cases,
            'continent': continent,
        }

        self.total_cases += cases
        self.total_new_cases += new_cases
        self.total_deaths += deaths
        self.total_new_deaths += new_deaths
        self.total_recovered += recovered
        self.total_critical_cases += critical_cases

    def __web_scrapper(self):

        url = 'https://www.worldometers.info/coronavirus/'

        res = requests.get(url)
        page = BeautifulSoup(res.content, 'html.parser')

        row_counter = 0
        for row in page.find(id='table3').find_all_next('tr'):
            row_data = []
            elements = row.find_all('td')
            for el in elements:
                try:
                    row_data.append(int(el.text.replace(',', '')))
                except ValueError:
                    text = el.text.replace(' ', '')
                    row_data.append(text if text != '' else 0)
            self.__add_data(row_data, row_counter)
            row_counter += 1

    @staticmethod
    def __calculate_death_percentage(confirmed, deaths):
        if confirmed is 0:
            deathly_percentage = 0
        else:
            deathly_percentage = deaths / confirmed * 100 if deaths is not 0 else 0

        return str(deathly_percentage)[:4]

    def __build_country(self, country):
        try:
            d = self.data.get(country)
            if d:
                rank = d.get('rank')
                date = d.get('date')
                cases = d.get('cases')
                new_cases = d.get('new_cases')
                deaths = d.get('deaths')
                new_deaths = d.get('new_deaths')
                recovered = d.get('recovered')
                critical_cases = d.get('critical_cases')
                continent = d.get('continent')

                out = '**#{} {}**\n'.format(rank, country.upper())

                out += 'Ultimo aggiornamento: {}\n'.format(date)
                out += 'Infetti: {}\n'.format(cases)
                out += 'Morti: {}\n'.format(deaths)
                out += 'Guariti: {}\n'.format(recovered)

                deathly_percentage = self.__calculate_death_percentage(cases, deaths)
                out += 'Mortalità attuale: {}%\n\n'.format(str(deathly_percentage)[:5])
                return out
            else:
                return ''
        except Exception as e:
            print(e)
            return ''

    def void_arg(self):

        out = '**Coronavirus Update**\n\n'
        out += 'Da dove vengono presi i dati:\n'
        out += 'https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6\n'
        out += 'https://www.worldometers.info/coronavirus/\n\n'
        out += 'Totale Infetti: {}\n'.format(self.total_cases)
        out += 'Nuovi Infetti: {}\n'.format(self.total_new_cases)
        out += 'Totale Morti: {}\n'.format(self.total_deaths)
        out += 'Nuovi Morti: {}\n'.format(self.total_new_deaths)
        out += 'Totale Guariti: {}\n'.format(self.total_recovered)
        out += 'Casi Critici: {}\n'.format(self.total_critical_cases)

        deathly_percentage = self.__calculate_death_percentage(self.total_cases, self.total_deaths)
        out += 'La mortalità attuale è del {}%'.format(str(deathly_percentage)[:5])

        print(out)
        # self.bot.send_message(out, MSG_ON_SAME_CHAT, parse_mode_en=True)

        # countries to stamp data
        my_country = ['italy', 'japan']
        out = ''
        for country in my_country:
            out += self.__build_country(country)

        print(out)
        # self.bot.send_message(out, MSG_ON_SAME_CHAT, parse_mode_en=True)

    def custom_country(self, country):
        out = self.__build_country(country)
        print(out)
        # self.bot.send_message(out, MSG_ON_SAME_CHAT, parse_mode_en=True)

    def run(self):

        self.__web_scrapper()
        pprint(self.data)

        """
        try:
            if self._sort.lower() == ('c' or 'confirmed' or 'infetti'):
                self.bot.send_message(self.__build_country_list('confirmed'), MSG_ON_SAME_CHAT, parse_mode_en=True)
                return

            if self._sort.lower() == ('r' or 'recovered' or 'guariti'):
                self.bot.send_message(self.__build_country_list('recovered'), MSG_ON_SAME_CHAT, parse_mode_en=True)
                return

            if self._sort.lower() == ('d' or 'deaths' or 'morti'):
                self.bot.send_message(self.__build_country_list('deaths'), MSG_ON_SAME_CHAT, parse_mode_en=True)
                return

        except AttributeError:
            pass
        
        """

        chose = {
            '': self.void_arg,
        }
        try:
            chose[self.arg]()
        except KeyError:
            self.custom_country(self.arg.lower())


if __name__ == '__main__':
    i = Scrapper()
    i.run()
