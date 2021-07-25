from binance.client import Client
from sys import argv
from time import sleep
from datetime import datetime

key_api = argv[1]
key_secret = argv[2]
client = Client(key_api, key_secret, tld='us')

is_running = True
max_loops = 10
loop_counter = 0

print('Program starting...')
while is_running and loop_counter < max_loops:
    print('Loop number: %i' % loop_counter)

    # main code
    exchange_info = client.get_exchange_info()
    server_time = int(exchange_info['serverTime']) // 1000
    readable_time = datetime.fromtimestamp(server_time)
    print("The server time is: %s" % readable_time)

    loop_counter += 1
    sleep(60)
else:
    print('Program ending')