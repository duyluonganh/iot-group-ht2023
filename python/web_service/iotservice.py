from random import random, randint


def get_humidity(): #call rasberi Pi to get humidity
    humidity = randint(30, 100)
    return humidity

def get_temperature():
    temperature = randint(-10, 20)
    return temperature
