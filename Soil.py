import random as rnd
import numpy as np
from Rain import Rain
import threading
from matplotlib import pyplot as plt
import time


class Soil:
    LAYERS_SIZE = []
    NUMBER_OF_LAYERS = 5
    LAYERS_PENETRATION = []
    TIME = 0
    DAY_LIMIT_TIME = 20
    DAY = 0
    MONTH = 0
    SEASON = 'spring'
    SEASONS = ['winter', 'winter', 'spring', 'spring', 'spring', 'summer', 'summer', 'summer', 'autumn', 'autumn',
               'autumn', 'winter']
    SPEED = 0
    # Specific properties of Soil
    VALVE_CAPACITY = 40
    IS_WATERING = False
    LAYERS_MOISTURE = []
    RAIN_CHANCE = 0.2
    SEASON_CHANGING_RAIN_MUTATION = {'spring': +.02 , 'summer': -.01 , 'autumn': +0.01, 'winter': +0.01}
    SEASON_CHANGING_PENETRATION = {'spring': +.01, 'summer': +.04, 'autumn': +.0, 'winter': -.4}
    CHANGING_PENETRATION_CHANCE = 0.02
    DAY_EVAPORATE_BASE = 0.02
    DAY_EVAPORATE_ERROR = 0.008
    NIGHT_EVAPORATE_BASE = 0.001
    NIGHT_EVAPORATE_ERROR = 0.008

    input_water = 0

    def __init__(self):
        self.LAYERS_PENETRATION = [np.random.rand() for i in range(self.NUMBER_OF_LAYERS)]
        self.LAYERS_MOISTURE = [np.random.rand() for i in range(self.NUMBER_OF_LAYERS)]
        self.LAYERS_SIZE = [np.random.rand()*50 for i in range(self.NUMBER_OF_LAYERS)]
        self.rain = Rain(time_limit=100, intensity=3, speed=0.1)
        '''
        self.LAYERS_PENETRATION = [0.5, 0.5, 0.5, 0.5]
        self.LAYERS_MOISTURE = [0.7, 0.2, 0.1, 0.0]
        self.LAYERS_SIZE = [70, 80, 90, 90]
        '''

    def irrigation_handler(self):
        all_data = []
        counter = 0
        while self.DAY < 3:
            self.irrigate()
            counter = counter +1
            all_data.append(self.LAYERS_MOISTURE.copy())
            print(self.LAYERS_MOISTURE)
            '''
            print('TIME: '+str(self.TIME) + ' , DAY: '+str(self.DAY)+' , MONTH: '+
                  str(self.MONTH)+' , SEASON: '+str(self.SEASON) + ' , RAINING: ' + str(self.rain.active)+
                  ' , RAINING_TIME_LIMIT: ' + str(self.rain.time_limit))
            for j in range(0, s.NUMBER_OF_LAYERS):
                print(str(s.LAYERS_MOISTURE[j]) + " , " + str(s.LAYERS_SIZE[j]) + " , " + str(s.LAYERS_PENETRATION[j]))
            print()
            time.sleep(1)
            '''
        all_data = np.array(all_data)
        time_axis = np.arange(0, counter)
        print(all_data)
        for i in range(0, self.NUMBER_OF_LAYERS):
            plt.plot(time_axis, all_data[:, i], label='layer '+str(i))
            plt.xlabel('time')
            plt.ylabel('moisture')
        plt.legend()
        plt.show()

    # Calender
    def increase_time(self):
        if self.TIME >= self.DAY_LIMIT_TIME:
            self.TIME = 0
            self.DAY += 1
            if self.DAY >= 30:
                self.DAY = 0
                self.MONTH += 1
                self.SEASON = self.SEASONS[self.MONTH]
                if self.MONTH >= 12:
                    self.MONTH = 0
        else:
            self.TIME += 1

    def penetration_mutation(self,*args):
        for i in range(self.NUMBER_OF_LAYERS):
            self.LAYERS_PENETRATION[i] = self.LAYERS_PENETRATION[i] if np.random.rand() > self.CHANGING_PENETRATION_CHANCE \
                else (self.LAYERS_PENETRATION[i] + np.random.rand()) / 2

    def rain_operation(self):
        if not self.rain.active:
            self.rain.start_rain(self.RAIN_CHANCE + self.SEASON_CHANGING_RAIN_MUTATION[self.SEASON])
        if self.rain.active:
            self.input_water += self.rain.rain()
        if self.IS_WATERING:
            self.input_water += self.VALVE_CAPACITY

    def make_mutation(self):
        self.penetration_mutation()
        self.rain_operation()

    def start_penetration(self):
        # first layer
        if self.input_water > self.LAYERS_SIZE[0]*(1 - self.LAYERS_MOISTURE[0]):
            self.input_water -= self.LAYERS_SIZE[0]*(1 - self.LAYERS_MOISTURE[0])
            self.LAYERS_MOISTURE[0] = 1
        else:
            self.input_water = 0
            self.LAYERS_MOISTURE[0] =(self.LAYERS_SIZE[0]*self.LAYERS_MOISTURE[0] + self.input_water) / self.LAYERS_SIZE[0]
        # other layers
        for i in range(self.NUMBER_OF_LAYERS-1, 0, -1):
            passed_water = self.LAYERS_MOISTURE[i-1]*self.LAYERS_SIZE[i-1]*self.LAYERS_PENETRATION[i-1]
            if passed_water > self.LAYERS_SIZE[i]*(1-self.LAYERS_MOISTURE[i]):
                passed_water = self.LAYERS_SIZE[i]*(1-self.LAYERS_MOISTURE[i])
            self.LAYERS_MOISTURE[i] += passed_water/self.LAYERS_SIZE[i]
            self.LAYERS_MOISTURE[i-1] -= passed_water/self.LAYERS_SIZE[i-1]

    def decorator(func):
        def wrapper(self, *args):
            self.increase_time()
            return func(self, args)
        return wrapper

    @decorator
    def irrigate(self, *args):
        self.make_mutation()
        self.start_penetration()


s = Soil()
t = threading.Thread(target=Soil.irrigation_handler(s))
t.start()
