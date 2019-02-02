import csv

from filtering_csv import (
    get_data_from_csv_file,
    sum_up_numbers_of_clicks_removing_repeated,
    generate_csv_file,
    csv_filter
)



def test_get_data_from_csv_file():
    expected_result = [
        {
            'date': '2019-01-21',
            'country_code': 'GIN',
            'impressions': 883,
            'number_of_clicks': 3
        },
        {
            'date': '2019-01-21',
            'country_code': 'GIN',
            'impressions': 76,
            'number_of_clicks': 1
        },
        {
            'date': '2019-01-21',
            'country_code': 'AFG',
            'impressions': 919,
            'number_of_clicks': 6
        }, {
            'date': '2019-01-22',
            'country_code': 'GIN',
            'impressions': 201,
            'number_of_clicks': 2
        },
        {
            'date': '2019-01-22',
            'country_code': 'CZE',
            'impressions': 139,
            'number_of_clicks': 1
        },
        {
            'date': '2019-01-22',
            'country_code': 'GIN',
            'impressions': 1050,
            'number_of_clicks': 10
        },
        {
            'date': '2019-01-23',
            'country_code': 'XXX',
            'impressions': 777,
            'number_of_clicks': 2
        },
        {
            'date': '2019-01-23',
            'country_code': 'GIN',
            'impressions': 72,
            'number_of_clicks': 1
        },
        {
            'date': '2019-01-23',
            'country_code': 'GIN',
            'impressions': 521,
            'number_of_clicks': 1
        },
        {
            'date': '2019-01-24',
            'country_code': 'CZE',
            'impressions': 620,
            'number_of_clicks': 1
        },
        {
            'date': '2019-01-24',
            'country_code': 'XXX',
            'impressions': 586,
            'number_of_clicks': 5
        },
        {
            'date': '2019-01-24',
            'country_code': 'XXX',
            'impressions': 1082,
            'number_of_clicks': 7
        }
    ]

    file_csv_name_in = 'test\\test_in_file_1.csv'
    assert get_data_from_csv_file(file_csv_name_in) == expected_result


def test_sum_up_numbers_of_clicks_removing_repeated():
    expected_result = {
        '2019-01-21': {
            'AFG': {'impressions': 919, 'number_of_clicks': 6},
            'GIN': {'impressions': 959, 'number_of_clicks': 4}
        },
        '2019-01-22': {
            'CZE': {'impressions': 139, 'number_of_clicks': 1},
            'GIN': {'impressions': 1251, 'number_of_clicks': 12}
        },
        '2019-01-23': {
            'GIN': {'impressions': 593, 'number_of_clicks': 2},
            'XXX': {'impressions': 777, 'number_of_clicks': 2}
        },
        '2019-01-24': {
            'CZE': {'impressions': 620, 'number_of_clicks': 1},
            'XXX': {'impressions': 1668, 'number_of_clicks': 12}
        }
    }
    file_csv_name_in = 'test\\test_in_file_2.csv'
    key = get_data_from_csv_file(file_csv_name_in)
    assert sum_up_numbers_of_clicks_removing_repeated(key) == expected_result


def test_generate_csv_file():
    expected_result = [
        ['2019-01-21', 'AFG', '919', '6'],
        ['2019-01-21', 'GIN', '959', '4'],
        ['2019-01-22', 'CZE', '139', '1'],
        ['2019-01-22', 'GIN', '1251', '12'],
        ['2019-01-23', 'GIN', '593', '2'],
        ['2019-01-23', 'XXX', '777', '2'],
        ['2019-01-24', 'CZE', '620', '1'],
        ['2019-01-24', 'XXX', '1668', '12']
    ]
    file_csv_name_in = 'test\\test_in_file_3.csv'
    file_csv_name_out = 'test\\test_out_file_3.csv'
    data = get_data_from_csv_file(file_csv_name_in)
    result = sum_up_numbers_of_clicks_removing_repeated(data)
    generate_csv_file(result, file_csv_name_out)
    with open(file_csv_name_out, 'r', encoding="utf-8") as f:
        reader = csv.reader(f)
        for index, row in enumerate(reader):
            assert row == expected_result[index]


def test_csv_filter():
    expected_result = [
        ['2019-01-21', 'AFG', '919', '6'],
        ['2019-01-21', 'GIN', '959', '4'],
        ['2019-01-22', 'CZE', '139', '1'],
        ['2019-01-22', 'GIN', '1251', '12'],
        ['2019-01-23', 'GIN', '593', '2'],
        ['2019-01-23', 'XXX', '777', '2'],
        ['2019-01-24', 'CZE', '620', '1'],
        ['2019-01-24', 'XXX', '1668', '12']
    ]
    file_csv_name_in = 'test\\test_in_file_4.csv'
    file_csv_name_out = 'test\\test_out_file_4.csv'

    csv_filter(file_csv_name_in, file_csv_name_out)

    with open(file_csv_name_out, 'r', encoding="utf-8") as f:
        reader = csv.reader(f)
        for index, row in enumerate(reader):
            assert row == expected_result[index]
