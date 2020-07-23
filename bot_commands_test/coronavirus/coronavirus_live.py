import json
from datetime import datetime
from pprint import pprint
import requests


class Scrapper(object):

    def __init__(self):
        # Counters for total data
        self.total_confirmed = 0
        self.total_recovered = 0
        self.total_deaths = 0

    def web_scrapper(self):

        section = 'services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/1/'
        query = 'where=Confirmed%20%3E%200&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*'
        order_by = 'orderByFields=Confirmed%20desc%2CCountry_Region%20asc%2CProvince_State%20asc&outSR=102100'
        url = 'https://{}query?f=json&{}&{}'.format(
            section,
            query,
            order_by,
        )

        content = requests.get(url).content
        json_data = json.loads(content)

        # get the main object
        data_list = json_data.get('features')

        country_data = {}

        for data in data_list:
            report = data.get('attributes')

            county = report.get('Country_Region')
            date = datetime.fromtimestamp(report.get('Last_Update') / 1e3)
            confirmed = report.get('Confirmed')
            recovered = report.get('Recovered')
            deaths = report.get('Deaths')

            self.total_confirmed += confirmed
            self.total_recovered += recovered
            self.total_deaths += deaths

            # create or update for sub zones
            try:
                d = country_data[county]
                d['date'] = date
                d['confirmed'] += confirmed
                d['recovered'] += recovered
                d['deaths'] += deaths
                country_data[county] = d

            except KeyError:
                country_data[county] = {
                    'date': date,
                    'confirmed': confirmed,
                    'recovered': recovered,
                    'deaths': deaths,
                }

        pprint(country_data)
        return country_data

    def main(self):

        # url = 'services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/cases_time_v3/FeatureServer/0/query?f=json'
        # where = 'where=1%3D1&outFields=*'
        # order_by = 'orderByFields=Report_Date_String'

        country_data = self.web_scrapper()

        out = '**Coronavirus Update**\n\n'
        out += 'Totale Confermati: {}\n'.format(self.total_confirmed)
        out += 'Totale Morti: {}\n'.format(self.total_deaths)
        out += 'Totale Guariti: {}\n\n'.format(self.total_recovered)

        deathly_percentage = self.total_deaths / self.total_recovered * 100
        out += 'La mortalità attuale è del {}%'.format(str(deathly_percentage)[:5])

        print(out)

        # countries to stamp data
        my_country = ['Mainland China', 'Italy', 'Japan', 'South Korea']
        for country in my_country:
            out = '**Coronavirus {}**\n\n'.format(country)
            d = country_data.get(country)
            if d:
                confirmed = d.get('confirmed')
                recovered = d.get('recovered')
                deaths = d.get('deaths')

                out += 'Confermati: {}\n'.format(confirmed)
                out += 'Morti: {}\n'.format(recovered)
                out += 'Guariti: {}\n\n'.format(deaths)

                deathly_percentage = deaths / recovered * 100 if deaths is not 0 else 0
                out += 'La mortalità attuale è del {}%'.format(str(deathly_percentage)[:5])

                print(out)


if __name__ == '__main__':
    i = Scrapper()
    i.main()
