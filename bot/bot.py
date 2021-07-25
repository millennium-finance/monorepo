from binance.client import Client
from sys import argv

key_api = argv[1]
key_secret = argv[2]
client = Client(key_api, key_secret)
is_running = True
max_loops = 10
loop_counter = 0
while is_running and loop_counter < max_loops:
    print('Hello, World! I am a bot and I am running. %i' % loop_counter)
    loop_counter += 1
else:
    print('Goodbye, World!')