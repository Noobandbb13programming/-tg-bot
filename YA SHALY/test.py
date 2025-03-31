import random
import time

i = True
number = 0

while i:
    time.sleep(1)
    msg = random.choice((
        'ЕБАТЬ!!',
         'ПИЗДЕЦ',
         'ДА НУ НАХУЙ',
         'Я В АХУЕ'
    ))
    print(msg)
    number += 1
    print(number)

    if number == 15:
        i = False
        print("Я устал я ухожу")
