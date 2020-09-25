import json
from helper.variable import day_in_week_trans, month_trans, devices, second_to_period, \
    day_to_period, hour_to_period, minus_to_period, year_to_period, month_to_period


class CleanData:
    def __init__(self, raw_data):
        self.data = json.loads(raw_data)

    def get_attribute(self, list_name_attribute):
        temp = self.data
        for attribute in list_name_attribute:
            temp = temp[attribute]
            if attribute == 'created_at':
                temp = convert_date(temp)
            elif attribute == 'source':
                temp = filter_device(temp)
        return temp

    def print_data(self):
        print(self.data)
        return

    def get_text(self):
        data = self.data
        if 'extended_tweet' in data:
            data = data['extended_tweet']
            data = data['full_text']
        elif 'retweeted_status' in data:
            data = data['retweeted_status']
            if 'extended_tweet' in data:
                data = data['extended_tweet']
                data = data['full_text']
            else:
                data = data['text']
        else:
            # print(data)
            data = data['text']
        return data


def convert_date(date_str):
    # date_str form: Day_in_week month day time(00:00:00) +0000 year
    date = list(date_str.split(' '))
    day_in_week = day_in_week_trans[date[0]]
    month = month_trans[date[1]]
    day = int(date[2])
    hour, minus, second = map(int, date[3].split(':'))
    year = int(date[-1])
    id_date = convert_time(second, minus, hour, day, month, year)
    return [str(id_date), str(month), str(day), str(year),
            str(hour), str(minus), str(second // 10), day_in_week]


def filter_device(source):
    for device in devices:
        if source.find(device) != -1:
            return device
    return 'Unknown'


def clean_text(text):
    quote = "\'"
    quote_in_text = "\'\'"
    text = text.replace(quote, quote_in_text)
    return quote + text + quote


def convert_to_string(data):
    if type(data) == str or data is None:
        if data is None:
            data = ""
        return clean_text(data)
    elif type(data) != list:
        return str(data)
    else:
        return data


def convert_time(second, minus, hour, day, month, year):
    time = second // second_to_period + minus * minus_to_period + hour * hour_to_period + \
           day * day_to_period + month * month_to_period + year * year_to_period
    return time


def convert_time_to_each10s(date):
    date = str(date)
    days, time = date.split(' ')
    year, month, day = map(int, days.split('-'))
    hour, minute, second = map(float, time.split(':'))
    second = int(second)
    period = convert_time(second, minute, hour, day, month, year)
    return period
