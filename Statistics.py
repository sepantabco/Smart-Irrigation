from FileOperations import FileOperation as FO_Operators
from SortCoordination import SortCoordination as SC_Operators
import pandas as pd
import math


class Statistics:

    def __init__(self):
        pass

    @staticmethod
    def classify_by_station():
        data = pd.read_csv('test_path/sorted_data_without_nan.txt')
        df = pd.DataFrame(data)
        temp = df.sort_values(by=['Network', 'radius'])
        previous_network = ''
        previous_distance = 33
        f = open('junk.txt', 'a')
        spoiled = False
        for index, row in temp.iterrows():
            if previous_network != row['Network'] or spoiled:
                previous_network = row['Network']
                spoiled = False
            else:
                if (previous_distance > math.pow((math.pow(float(row['lat'].replace("\'", "").replace(" ", "")),
                                                           2) + math.pow(
                    float(row['lon'].replace("\'", "").replace(" ", "")), 2)), 0.5) + 10) or (
                        previous_distance < math.pow((math.pow(float(row['lat'].replace("\'", "").replace(" ", "")),
                                                               2) + math.pow(
                    float(row['lon'].replace("\'", "").replace(" ", "")), 2)), 0.5) - 10):
                    f.writelines(row['Network'])
                    spoiled = True
                    print(row['Network'])
                    print(row['radius'])
                previous_distance = math.pow((math.pow(float(row['lat'].replace("\'", "").replace(" ", "")),
                                                       2) + math.pow(
                    float(row['lon'].replace("\'", "").replace(" ", "")), 2)), 0.5)
        f.close()

