from os import path
import pandas
from binance.client import Client
from dateutil import parser as date_parser
from datetime import datetime
import time

TIMESTAMP = 'timestamp'
BTCUSDT = 'BTCUSDT'

BTCDOWNUSDT = 'BTCDOWNUSDT'

BTCBTCDOWN = 'BTCBTCDOWN'

days_of_data = 100

'''
TODO: Take out the credentials and make the simulations run without them or hide the credentials from version
control
'''


def create_binance_client():
    read_mode = str('r')
    credentials_file_name = str('creds.txt')
    new_line_character = str('\n')
    empty_string = str("")

    info = [line.replace(new_line_character, empty_string) for line in
            open(credentials_file_name, read_mode).readlines()]
    api_key = info[0]
    api_secret = info[1]

    return Client(api_key, api_secret)


def get_data_frame_BTC_1m(binance_client):
    seconds_in_a_day = int(86400)
    number_of_days_back = int(days_of_data)
    current_timestamp = int(time.time())
    previous_timestamp = int(current_timestamp - seconds_in_a_day * number_of_days_back)
    previous_date = datetime.fromtimestamp(previous_timestamp).strftime('%d %b %Y')

    def get_time_duration(crypto_symbol, interval, existing_data_frame):
        if len(existing_data_frame) > 0:
            oldest_timestamp = date_parser.parse(existing_data_frame["timestamp"].iloc[-1])
        else:
            oldest_timestamp = datetime.strptime(f'{previous_date}', '%d %b %Y')

        binance_k_lines = binance_client.get_klines(symbol=crypto_symbol, interval=interval)
        newest_timestamp = pandas.to_datetime(binance_k_lines[-1][0], unit="ms")
        return oldest_timestamp, newest_timestamp

    def get_all_binance(crypto_symbol, interval, save=False):
        data_directory = str('data_BTC')
        data_file_name = path.join(data_directory, f'{crypto_symbol}_m.csv')

        if path.isfile(data_file_name):
            file_data_frame = pandas.read_csv(data_file_name)
        else:
            file_data_frame = pandas.DataFrame()

        oldest_point, newest_point = get_time_duration(crypto_symbol, interval, file_data_frame)
        time_format = str("%d %b %Y %H:%M:%S")
        formatted_oldest_point = str(oldest_point.strftime(time_format))
        formatted_newest_point = str(newest_point.strftime(time_format))

        columns = [
            TIMESTAMP,
            'open',
            'high',
            'low',
            'close',
            'volume',
            'close_time',
            'quote_av',
            'trades',
            'tb_base_av',
            'tb_quote_av',
            'ignore'
        ]
        historical_k_lines = binance_client \
            .get_historical_klines(crypto_symbol, interval, formatted_oldest_point, formatted_newest_point)
        data_frame = pandas.DataFrame(historical_k_lines, columns=columns)
        data_frame[TIMESTAMP] = pandas.to_datetime(data_frame[TIMESTAMP], unit='ms')
        if len(file_data_frame) > 0:
            temporary_data_frame = pandas.DataFrame(data_frame)
            file_data_frame = file_data_frame.append(temporary_data_frame)
        else:
            file_data_frame = data_frame

        file_data_frame.set_index(TIMESTAMP, inplace=True)
        if save:
            file_data_frame.to_csv(data_file_name)
        return pandas.read_csv(path.join(data_directory, f'{BTCUSDT}_m.csv'))

    return get_all_binance(BTCUSDT, '1m', save=True)


def get_data_frame_BTC_15m(binance_client):
    seconds_in_a_day = int(86400)
    number_of_days_back = int(days_of_data)
    current_timestamp = int(time.time())
    previous_timestamp = int(current_timestamp - seconds_in_a_day * number_of_days_back)
    previous_date = datetime.fromtimestamp(previous_timestamp).strftime('%d %b %Y')

    def get_time_duration(crypto_symbol, interval, existing_data_frame):
        if len(existing_data_frame) > 0:
            oldest_timestamp = date_parser.parse(existing_data_frame["timestamp"].iloc[-1])
        else:
            oldest_timestamp = datetime.strptime(f'{previous_date}', '%d %b %Y')

        binance_k_lines = binance_client.get_klines(symbol=crypto_symbol, interval=interval)
        newest_timestamp = pandas.to_datetime(binance_k_lines[-1][0], unit="ms")
        return oldest_timestamp, newest_timestamp

    def get_all_binance(crypto_symbol, interval, save=False):
        data_directory = str('data_BTC')
        data_file_name = path.join(data_directory, f'{crypto_symbol}_15m.csv')

        if path.isfile(data_file_name):
            file_data_frame = pandas.read_csv(data_file_name)
        else:
            file_data_frame = pandas.DataFrame()

        oldest_point, newest_point = get_time_duration(crypto_symbol, interval, file_data_frame)
        time_format = str("%d %b %Y %H:%M:%S")
        formatted_oldest_point = str(oldest_point.strftime(time_format))
        formatted_newest_point = str(newest_point.strftime(time_format))

        columns = [
            TIMESTAMP,
            'open',
            'high',
            'low',
            'close',
            'volume',
            'close_time',
            'quote_av',
            'trades',
            'tb_base_av',
            'tb_quote_av',
            'ignore'
        ]
        historical_k_lines = binance_client \
            .get_historical_klines(crypto_symbol, interval, formatted_oldest_point, formatted_newest_point)
        data_frame = pandas.DataFrame(historical_k_lines, columns=columns)
        data_frame[TIMESTAMP] = pandas.to_datetime(data_frame[TIMESTAMP], unit='ms')
        if len(file_data_frame) > 0:
            temporary_data_frame = pandas.DataFrame(data_frame)
            file_data_frame = file_data_frame.append(temporary_data_frame)
        else:
            file_data_frame = data_frame

        file_data_frame.set_index(TIMESTAMP, inplace=True)
        if save:
            file_data_frame.to_csv(data_file_name)
        return pandas.read_csv(path.join(data_directory, f'{BTCUSDT}_15m.csv'))
        
    return get_all_binance(BTCUSDT, '15m', save=True)


def get_data_frame_BTC_12h(binance_client):
    seconds_in_a_day = int(86400)
    number_of_days_back = int(days_of_data)
    current_timestamp = int(time.time())
    previous_timestamp = int(current_timestamp - seconds_in_a_day * number_of_days_back)
    previous_date = datetime.fromtimestamp(previous_timestamp).strftime('%d %b %Y')

    def get_time_duration(crypto_symbol, interval, existing_data_frame):
        if len(existing_data_frame) > 0:
            oldest_timestamp = date_parser.parse(existing_data_frame["timestamp"].iloc[-1])
        else:
            oldest_timestamp = datetime.strptime(f'{previous_date}', '%d %b %Y')

        binance_k_lines = binance_client.get_klines(symbol=crypto_symbol, interval=interval)
        newest_timestamp = pandas.to_datetime(binance_k_lines[-1][0], unit="ms")

        return oldest_timestamp, newest_timestamp

    def get_all_binance(crypto_symbol, interval, save=False):
        data_directory = str('data_BTC')
        data_file_name = path.join(data_directory, f'{crypto_symbol}_12h.csv')

        if path.isfile(data_file_name):
            file_data_frame = pandas.read_csv(data_file_name)
        else:
            file_data_frame = pandas.DataFrame()

        oldest_point, newest_point = get_time_duration(crypto_symbol, interval, file_data_frame)
        time_format = str("%d %b %Y %H:%M:%S")
        formatted_oldest_point = str(oldest_point.strftime(time_format))
        formatted_newest_point = str(newest_point.strftime(time_format))

        columns = [
            TIMESTAMP,
            'open',
            'high',
            'low',
            'close',
            'volume',
            'close_time',
            'quote_av',
            'trades',
            'tb_base_av',
            'tb_quote_av',
            'ignore'
        ]
        historical_k_lines = binance_client \
            .get_historical_klines(crypto_symbol, interval, formatted_oldest_point, formatted_newest_point)
        data_frame = pandas.DataFrame(historical_k_lines, columns=columns)
        data_frame[TIMESTAMP] = pandas.to_datetime(data_frame[TIMESTAMP], unit='ms')
        if len(file_data_frame) > 0:
            temporary_data_frame = pandas.DataFrame(data_frame)
            file_data_frame = file_data_frame.append(temporary_data_frame)
        else:
            file_data_frame = data_frame

        file_data_frame.set_index(TIMESTAMP, inplace=True)
        if save:
            file_data_frame.to_csv(data_file_name)
        return pandas.read_csv(path.join(data_directory, f'{BTCUSDT}_12h.csv'))

    return get_all_binance(BTCUSDT, '12h', save=True)


    #pull 1 day data frame
def get_data_frame_BTC_1d(binance_client):
    seconds_in_a_day = int(86400)
    number_of_days_back = int(days_of_data)
    current_timestamp = int(time.time())
    previous_timestamp = int(current_timestamp - seconds_in_a_day * number_of_days_back)
    previous_date = datetime.fromtimestamp(previous_timestamp).strftime('%d %b %Y')

    def get_time_duration(crypto_symbol, interval, existing_data_frame):
        if len(existing_data_frame) > 0:
            oldest_timestamp = date_parser.parse(existing_data_frame["timestamp"].iloc[-1])
        else:
            oldest_timestamp = datetime.strptime(f'{previous_date}', '%d %b %Y')

        binance_k_lines = binance_client.get_klines(symbol=crypto_symbol, interval=interval)
        newest_timestamp = pandas.to_datetime(binance_k_lines[-1][0], unit="ms")

        return oldest_timestamp, newest_timestamp

    def get_all_binance(crypto_symbol, interval, save=False):
        data_directory = str('data_BTC')
        data_file_name = path.join(data_directory, f'{crypto_symbol}_d.csv')

        if path.isfile(data_file_name):
            file_data_frame = pandas.read_csv(data_file_name)
        else:
            file_data_frame = pandas.DataFrame()

        oldest_point, newest_point = get_time_duration(crypto_symbol, interval, file_data_frame)
        time_format = str("%d %b %Y %H:%M:%S")
        formatted_oldest_point = str(oldest_point.strftime(time_format))
        formatted_newest_point = str(newest_point.strftime(time_format))

        columns = [
            TIMESTAMP,
            'open',
            'high',
            'low',
            'close',
            'volume',
            'close_time',
            'quote_av',
            'trades',
            'tb_base_av',
            'tb_quote_av',
            'ignore'
        ]
        historical_k_lines = binance_client \
            .get_historical_klines(crypto_symbol, interval, formatted_oldest_point, formatted_newest_point)
        data_frame = pandas.DataFrame(historical_k_lines, columns=columns)
        data_frame[TIMESTAMP] = pandas.to_datetime(data_frame[TIMESTAMP], unit='ms')
        if len(file_data_frame) > 0:
            temporary_data_frame = pandas.DataFrame(data_frame)
            file_data_frame = file_data_frame.append(temporary_data_frame)
        else:
            file_data_frame = data_frame

        file_data_frame.set_index(TIMESTAMP, inplace=True)
        if save:
            file_data_frame.to_csv(data_file_name)
        return pandas.read_csv(path.join(data_directory, f'{BTCUSDT}_d.csv'))

    return get_all_binance(BTCUSDT, '1d', save=True)










def create_binance_client():
    read_mode = str('r')
    credentials_file_name = str('creds.txt')
    new_line_character = str('\n')
    empty_string = str("")

    info = [line.replace(new_line_character, empty_string) for line in
            open(credentials_file_name, read_mode).readlines()]
    api_key = info[0]
    api_secret = info[1]

    return Client(api_key, api_secret)


def get_data_frame_BTCDWN_1m(binance_client):
    seconds_in_a_day = int(86400)
    number_of_days_back = int(days_of_data)
    current_timestamp = int(time.time())
    previous_timestamp = int(current_timestamp - seconds_in_a_day * number_of_days_back)
    previous_date = datetime.fromtimestamp(previous_timestamp).strftime('%d %b %Y')

    def get_time_duration(crypto_symbol, interval, existing_data_frame):
        if len(existing_data_frame) > 0:
            oldest_timestamp = date_parser.parse(existing_data_frame["timestamp"].iloc[-1])
        else:
            oldest_timestamp = datetime.strptime(f'{previous_date}', '%d %b %Y')

        binance_k_lines = binance_client.get_klines(symbol=crypto_symbol, interval=interval)
        newest_timestamp = pandas.to_datetime(binance_k_lines[-1][0], unit="ms")
        return oldest_timestamp, newest_timestamp

    def get_all_binance(crypto_symbol, interval, save=False):
        data_directory = str('data_BTCDWN')
        data_file_name = path.join(data_directory, f'{crypto_symbol}_m.csv')

        if path.isfile(data_file_name):
            file_data_frame = pandas.read_csv(data_file_name)
        else:
            file_data_frame = pandas.DataFrame()

        oldest_point, newest_point = get_time_duration(crypto_symbol, interval, file_data_frame)
        time_format = str("%d %b %Y %H:%M:%S")
        formatted_oldest_point = str(oldest_point.strftime(time_format))
        formatted_newest_point = str(newest_point.strftime(time_format))

        columns = [
            TIMESTAMP,
            'open',
            'high',
            'low',
            'close',
            'volume',
            'close_time',
            'quote_av',
            'trades',
            'tb_base_av',
            'tb_quote_av',
            'ignore'
        ]
        historical_k_lines = binance_client \
            .get_historical_klines(crypto_symbol, interval, formatted_oldest_point, formatted_newest_point)
        data_frame = pandas.DataFrame(historical_k_lines, columns=columns)
        data_frame[TIMESTAMP] = pandas.to_datetime(data_frame[TIMESTAMP], unit='ms')
        if len(file_data_frame) > 0:
            temporary_data_frame = pandas.DataFrame(data_frame)
            file_data_frame = file_data_frame.append(temporary_data_frame)
        else:
            file_data_frame = data_frame

        file_data_frame.set_index(TIMESTAMP, inplace=True)
        if save:
            file_data_frame.to_csv(data_file_name)
        return pandas.read_csv(path.join(data_directory, f'{BTCDOWNUSDT}_m.csv'))

    return get_all_binance(BTCDOWNUSDT, '1m', save=True)


def get_data_frame_BTCDWN_12h(binance_client):
    seconds_in_a_day = int(86400)
    number_of_days_back = int(days_of_data)
    current_timestamp = int(time.time())
    previous_timestamp = int(current_timestamp - seconds_in_a_day * number_of_days_back)
    previous_date = datetime.fromtimestamp(previous_timestamp).strftime('%d %b %Y')

    def get_time_duration(crypto_symbol, interval, existing_data_frame):
        if len(existing_data_frame) > 0:
            oldest_timestamp = date_parser.parse(existing_data_frame["timestamp"].iloc[-1])
        else:
            oldest_timestamp = datetime.strptime(f'{previous_date}', '%d %b %Y')

        binance_k_lines = binance_client.get_klines(symbol=crypto_symbol, interval=interval)
        newest_timestamp = pandas.to_datetime(binance_k_lines[-1][0], unit="ms")

        return oldest_timestamp, newest_timestamp

    def get_all_binance(crypto_symbol, interval, save=False):
        data_directory = str('data_BTCDWN')
        data_file_name = path.join(data_directory, f'{crypto_symbol}_12h.csv')

        if path.isfile(data_file_name):
            file_data_frame = pandas.read_csv(data_file_name)
        else:
            file_data_frame = pandas.DataFrame()

        oldest_point, newest_point = get_time_duration(crypto_symbol, interval, file_data_frame)
        time_format = str("%d %b %Y %H:%M:%S")
        formatted_oldest_point = str(oldest_point.strftime(time_format))
        formatted_newest_point = str(newest_point.strftime(time_format))

        columns = [
            TIMESTAMP,
            'open',
            'high',
            'low',
            'close',
            'volume',
            'close_time',
            'quote_av',
            'trades',
            'tb_base_av',
            'tb_quote_av',
            'ignore'
        ]
        historical_k_lines = binance_client \
            .get_historical_klines(crypto_symbol, interval, formatted_oldest_point, formatted_newest_point)
        data_frame = pandas.DataFrame(historical_k_lines, columns=columns)
        data_frame[TIMESTAMP] = pandas.to_datetime(data_frame[TIMESTAMP], unit='ms')
        if len(file_data_frame) > 0:
            temporary_data_frame = pandas.DataFrame(data_frame)
            file_data_frame = file_data_frame.append(temporary_data_frame)
        else:
            file_data_frame = data_frame

        file_data_frame.set_index(TIMESTAMP, inplace=True)
        if save:
            file_data_frame.to_csv(data_file_name)
        return pandas.read_csv(path.join(data_directory, f'{BTCDOWNUSDT}_12h.csv'))

    return get_all_binance(BTCDOWNUSDT, '12h', save=True)


    #pull 1 day data frame
def get_data_frame_BTCDWN_1d(binance_client):
    seconds_in_a_day = int(86400)
    number_of_days_back = int(days_of_data)
    current_timestamp = int(time.time())
    previous_timestamp = int(current_timestamp - seconds_in_a_day * number_of_days_back)
    previous_date = datetime.fromtimestamp(previous_timestamp).strftime('%d %b %Y')

    def get_time_duration(crypto_symbol, interval, existing_data_frame):
        if len(existing_data_frame) > 0:
            oldest_timestamp = date_parser.parse(existing_data_frame["timestamp"].iloc[-1])
        else:
            oldest_timestamp = datetime.strptime(f'{previous_date}', '%d %b %Y')

        binance_k_lines = binance_client.get_klines(symbol=crypto_symbol, interval=interval)
        newest_timestamp = pandas.to_datetime(binance_k_lines[-1][0], unit="ms")

        return oldest_timestamp, newest_timestamp

    def get_all_binance(crypto_symbol, interval, save=False):
        data_directory = str('data_BTCDWN')
        data_file_name = path.join(data_directory, f'{crypto_symbol}_1d.csv')

        if path.isfile(data_file_name):
            file_data_frame = pandas.read_csv(data_file_name)
        else:
            file_data_frame = pandas.DataFrame()

        oldest_point, newest_point = get_time_duration(crypto_symbol, interval, file_data_frame)
        time_format = str("%d %b %Y %H:%M:%S")
        formatted_oldest_point = str(oldest_point.strftime(time_format))
        formatted_newest_point = str(newest_point.strftime(time_format))

        columns = [
            TIMESTAMP,
            'open',
            'high',
            'low',
            'close',
            'volume',
            'close_time',
            'quote_av',
            'trades',
            'tb_base_av',
            'tb_quote_av',
            'ignore'
        ]
        historical_k_lines = binance_client \
            .get_historical_klines(crypto_symbol, interval, formatted_oldest_point, formatted_newest_point)
        data_frame = pandas.DataFrame(historical_k_lines, columns=columns)
        data_frame[TIMESTAMP] = pandas.to_datetime(data_frame[TIMESTAMP], unit='ms')
        if len(file_data_frame) > 0:
            temporary_data_frame = pandas.DataFrame(data_frame)
            file_data_frame = file_data_frame.append(temporary_data_frame)
        else:
            file_data_frame = data_frame

        file_data_frame.set_index(TIMESTAMP, inplace=True)
        if save:
            file_data_frame.to_csv(data_file_name)
        return pandas.read_csv(path.join(data_directory, f'{BTCDOWNUSDT}_1d.csv'))

    return get_all_binance(BTCDOWNUSDT, '1d', save=True)

