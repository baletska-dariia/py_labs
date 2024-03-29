import math as math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from Tkinter import *

#------DATA-----#
class1 = np.array([[0.49, 0.89],
                   [0.34, 0.81],
                   [0.36, 0.67],
                   [0.47, 0.49],
                   [0.52, 0.53]])
class3 = np.array([[0.62, 0.83],
                   [0.79, 0.92],
                   [0.71, 0.92],
                   [0.78, 0.83],
                   [0.87, 0.92]])
class4 = np.array([[0.55, 0.4],
                   [0.66, 0.32],
                   [0.74, 0.49],
                   [0.89, 0.3],
                   [0.77, 0.02]])
class6 = np.array([[0.05, 0.15],
                   [0.09, 0.39],
                   [0.13, 0.51],
                   [0.25, 0.34],
                   [0.15, 0.36]])


class Calculations:
    #1.1
    def euclid_distance(self, class1, class2):
        dx = (class1[0] - class2[0]) ** 2
        dy = (class2[1] - class2[1]) ** 2
        d_euclid = math.sqrt(dx + dy)
        return d_euclid

    # 1.5
    def max_mod_distance(self, class1, class2):
        dx = math.fabs(class1[0] - class2[0])
        dy = math.fabs(class2[1] - class2[1])
        return max([dx, dy])

    # 2.1
    def calculate_distance_to_centroid(self, func, ePoint, centroid):
        d = func(ePoint, centroid)
        return d

    # 2.1 Util
    def find_centroid(self, eClass):
        xMean = np.mean(eClass[:, 0])
        yMean = np.mean(eClass[:, 1])
        return [xMean, yMean]

    # 2.5
    def calculate_two_minimal_distances(self, func, ePoint, eClass):
        distances = [np.array([])]
        for point in eClass:
            newDistance = func(ePoint, point)
            distances = np.append(distances, newDistance)
        return sum(np.sort(distances)[:2])


class UI:
    def __init__(self, window):
        self.window = window
        self.func1_state = IntVar()
        self.func2_state = IntVar()
        self.func3_state = IntVar()
        self.func4_state = IntVar()
        self.func1 = Checkbutton(window, text='(object-centroid) euclid_distance', var=self.func1_state)
        self.func2 = Checkbutton(window, text='(object-centroid) max_mod_distance', var=self.func2_state)
        self.func3 = Checkbutton(window, text='(object-object) euclid_distance', var=self.func3_state)
        self.func4 = Checkbutton(window, text='(object-object) max_mod_distance', var=self.func4_state)
        self.func1.pack()
        self.func2.pack()
        self.func3.pack()
        self.func4.pack()
        self.plot()

    def getColor(self, x, y):
        global result
        if x is not None and y is not None:
            calculations = Calculations()
            classes = [class1, class3, class4, class6]
            colors = ['*r', '*g', '*b', '*y']
            distances = [np.array([])]
            if self.func1_state.get() == 1:
                for c in classes:
                    d = calculations.calculate_distance_to_centroid(calculations.euclid_distance,
                                                                    [x, y], calculations.find_centroid(c))
                    distances = np.append(distances, d)
                    result = np.where(distances == min(distances))
                print(distances)
                print(result)
                return colors[result[0][0]]
            elif self.func2_state.get() == 1:
                for c in classes:
                    d = calculations.calculate_distance_to_centroid(calculations.max_mod_distance,
                                                                    [x, y], calculations.find_centroid(c))
                    distances = np.append(distances, d)
                    result = np.where(distances == min(distances))
                print(distances)
                print(result)
                return colors[result[0][0]]
            elif self.func3_state.get() == 1:
                for c in classes:
                    d = calculations.calculate_two_minimal_distances(calculations.euclid_distance,
                                                                     [x, y], c)
                    distances = np.append(distances, d)
                    result = np.where(distances == min(distances))
                print(distances)
                print(result)
                return colors[result[0][0]]
            elif self.func4_state.get() == 1:
                for c in classes:
                    d = calculations.calculate_two_minimal_distances(calculations.max_mod_distance,
                                                                     [x, y], c)
                    distances = np.append(distances, d)
                    result = np.where(distances == min(distances))
                print(distances)
                print(result)
                return colors[result[0][0]]

    def plot(self):
        fig = Figure(figsize=(6, 6))
        plt = fig.add_subplot(111)
        for i in enumerate(class1):
            p1, = plt.plot(class1[:, 0], class1[:, 1], '*r')
            p2, = plt.plot(class3[:, 0], class3[:, 1], '*g')
            p3, = plt.plot(class4[:, 0], class4[:, 1], '*b')
            p4, = plt.plot(class6[:, 0], class6[:, 1], '*y')

        plt.legend([p1, p2, p3, p4], ["class1", "class3", "class4", "class6"])
        plt.grid(True)

        def onclick(event):
            plt.plot(event.xdata, event.ydata, self.getColor(event.xdata, event.ydata))
            fig.canvas.draw()

        canvas = FigureCanvasTkAgg(fig, master=self.window)
        canvas.get_tk_widget().pack()
        canvas.draw()
        cid = canvas.mpl_connect('button_press_event', onclick)


window = Tk()
start = UI(window)
window.mainloop()
