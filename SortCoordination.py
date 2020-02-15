from FileOperations import FileOperation as FO_Operators


class SortCoordination:
    def __init__(self):
        pass

    SORTED_DATA = []

    def sorted_data_by_coordination(self):
        fo = FO_Operators()

        while not fo.END_OF_FILE:
            temp1 = fo.read_line()
            for x in temp1:
                if 'lon' in x:
                    continue
                temp2 = x.replace('\n', '')
                temp3 = temp2.split(',')
                temp3.append(self.compute_radius(float(temp3[7]), float(temp3[8])))
                self.SORTED_DATA.append(temp3)
        self.SORTED_DATA.sort(key=lambda y: float(y[9]))
        with open('C:\\Users\\Mahdi\\Desktop\\sorted_data.txt', 'w') as f:
            for item in self.SORTED_DATA:
                f.write("%s\n" % item)

    @staticmethod
    def compute_radius(x, y):
        return (x ** 2 + y ** 2) ** (1 / 2)

    @staticmethod
    def remove_useless_data():
        with open("C:\\Users\\Mahdi\\Desktop\\sorted_data.txt", "r") as f:
            lines = f.readlines()
        with open("C:\\Users\\Mahdi\\Desktop\\sorted_data_without_nan.txt", "w") as f:
            for line in lines:
                if line.find('\'nan\',') == -1:
                    print(line)
                    f.write(line)
