from binance.client import Client
from sys import argv

key_api = argv[1]
key_secret = argv[2]
client = Client(key_api, key_secret, tld='us')

is_running = True
max_loops = 1
loop_counter = 0

print('Program starting...')
while is_running and loop_counter < max_loops:
    print('Loop number: %i' % loop_counter)

    # main code
    exchange_info = client.get_exchange_info()
    print(exchange_info['symbols'][0]['symbol'])

    loop_counter += 1
else:
    print('Program ending')