from typing import TextIO
import csv
import re

TEMPLATE = '''
## Test {}

| ID | Categoria | Ultimo Test |
| --- | --- | --- |
| {} | {} | {} |

### Condizioni iniziali
{}

### Procedimento
{}

### Risultato atteso
{}
'''


class CsvReader:
    """Read the excel csw file and build the catalog structure"""
    def __init__(self):
        self.catalog = {}
    
    def read(self, csv_file: TextIO):
        """read the data from the csv, and """

        self.catalog = load_other_file()

        csv_data = csv.reader(csv_file, delimiter=';')

        bk_one = None
        bk_two = None
        bk_three = None
        bk_four = None
        bk_five = None

        for idx, row in enumerate(csv_data):
            # skip first, line
            if idx == 0:
                continue

            one = row[0]
            two = row[1]
            three = row[2]
            # three = re.sub('.*?_OK', '', row[2])
            four = row[3]
            five = row[4]
            six = row[5]
            seven = row[6]
            # eight = row[7]

            if one:
                bk_one = one
            else:
                one = bk_one

            if two:
                bk_two = two
            else:
                two = bk_two
            
            if three:
                bk_three = three
            else:
                three = bk_three

            if four:
                bk_four = four
            else:
                four = bk_four
            
            if five:
                bk_five = five
            else:
                five = bk_five


            with open('catalog3.data', 'a') as file:
                """
                file.write(TEMPLATE.format(
                    one,
                    one,
                    two,  # category
                    seven,  # success status
                    three,  # initial
                    four,  # in
                    five  # out
                ))
                """

                file.write( f'| {five+seven} | {six} | {four} | {three} | {two} | {one} |\n')
                
def load_other_file():
    out = {}
    with open('catalog.data', 'r') as file:
        for line in file.readlines():
            country, code = line.split('.')
            out[country] = code

    return out


                
if __name__ == '__main__':
    cr = CsvReader()
    with open('tassonomia.csv', 'r', encoding='latin') as file:
        cr.read(file)
    
    """import json
    with open('catalog.data', 'w') as file:
        file.write(cr.catalog)"""