is_running = True
loop_counter = 1
while is_running and loop_counter <= 10:
    print('Hello, World! I am a bot and I am running. %i' % loop_counter)
    loop_counter += 1
else:
    print('Goodbye, World!')