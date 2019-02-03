import pycountry
import csv
import sys
import logging
from datetime import datetime
from operator import itemgetter


infile_csv_name = 'csv_input_file.csv'
outfile_csv_name = 'csv_output_file.csv'


def csv_filter(infile_name, outfile_name):
    """
    The function rewrites data to the company standard
    :param infile_name:
    Name of the file with its prefix .csv from which data is taken
    :param outfile_name:
    Name of the file with its suffix .csv to which data is to be generated
    """
    data = get_data_from_csv_file(infile_name)
    result = sum_up_numbers_of_clicks_removing_repeated(data)
    generate_csv_file(result, outfile_name)


def get_data_from_csv_file(infile_name):
    """
    Opens file with n rows and puts data in n-elements list within dictionaries
    :return:
    n-elements list of dictionaries
    [{ 'date': 'YYYY-MM-DD', 'country_code': '3 char code', 'impressions': int, 'number_of_clicks': int }]
    """
    try:
        with open(infile_name, 'r', encoding="utf-8") as f:
            reader = csv.reader(f)
            data = []
            for row in reader:
                date, state_name, impressions, ctr = row
                country_code = None
                date = datetime.strptime(date, "%m/%d/%Y")
                date = date.strftime("%Y-%m-%d")

                for subdivision in pycountry.subdivisions:
                    if subdivision.name == state_name:
                        country_code = subdivision.country.alpha_3
                        break

                if country_code is None:
                    country_code = 'XXX'

                impressions = int(impressions)
                if ctr.endswith('%'):
                    ctr = float(ctr.replace('%', ''))/100

                number_of_clicks = round(impressions * ctr)

                data.append({'date': date,
                             'country_code': country_code,
                             'impressions': impressions,
                             'number_of_clicks': number_of_clicks})

            return data

    except FileNotFoundError:
        logging.error('File not found')
        sys.exit()


def sum_up_numbers_of_clicks_removing_repeated(data):
    """
    Makes operations to sort and sum up impressions and number of clicks to specified date and country code
    :param data: Accepts list of n-elements list with dictionaries
    [{ 'date': 'YYYY-MM-DD', 'country_code': '3 char code', 'impressions': int, 'number_of_clicks': int }, {...}]
    :return:
    Returns filled, sorted, nested dictionary
    result = {
        'YYYY-MM-DD': {
            '3 char code': {
                'impressions': int,
                 'number_of_clicks': int
            },
            '3 char code': {...}
        },
        'YYYY-MM-DD': {...}
    }
    """
    data = sorted(data, key=itemgetter('date', 'country_code'))
    help_set_dates = {x['date'] for x in data}              # Help sets are used to create dictionary and sorting
    help_set_codes = {x['country_code'] for x in data}      # before adding values in order to avoid errors

    help_set_dates = sorted(help_set_dates)
    help_set_codes = sorted(help_set_codes)

    result = {date: {} for date in help_set_dates}
    for date in help_set_dates:
        for code in help_set_codes:
            result[date][code] = {'impressions': 0, 'number_of_clicks': 0}

    for element in data:                                    # Filtering impressions and number of clicks to
        try:                                                # specified place in dictionary
            result[element['date']][element['country_code']]['impressions'] += int(element['impressions'])
            result[element['date']][element['country_code']]['number_of_clicks'] += int(element['number_of_clicks'])
        except IndexError:
            logging.warning('Index comes over limit')
            pass
    for date in help_set_dates:                             # Removing empty dictionaries from the result
        for code in help_set_codes:
            if result[date][code]['impressions'] == 0 and result[date][code]['number_of_clicks'] == 0:
                try:
                    del result[date][code]
                except KeyError:
                    logging.warning('There is no key value for that')
                    pass
    return result


def generate_csv_file(data, outfile_name):
    """
    Generates .csv file from the given data
    :param data:
    Gets filled, sorted, nested dictionary
    data = {
        'YYYY-MM-DD': {
            '3 char code': {
                'impressions': int,
                 'number_of_clicks': int
            },
            '3 char code': {...}
        },
        'YYYY-MM-DD': {...}
    }
    :param outfile_name:
    Name of the file with its suffix .csv to which data is to be generated
    :return:
    Returns n rows of text of specified look to the .csv file
    YYYY-MM-DD, 3 char code, number of impressions, number of clicks
    """
    with open(outfile_name, mode='w', newline='') as file:
        data_writer = csv.writer(file, delimiter=',')

        for date in data:
            for code in data[date]:
                data_writer.writerow([
                    date,
                    code,
                    data[date][code]['impressions'],
                    data[date][code]['number_of_clicks']])


if __name__ == '__main__':
    csv_filter(infile_csv_name, outfile_csv_name)
