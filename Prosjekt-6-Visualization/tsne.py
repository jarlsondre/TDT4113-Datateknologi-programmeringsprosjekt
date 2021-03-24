import numpy as np
import random



class TSNE():

    def __init__(self, max_iteration = 20):
        self.data = None
        self.max_iteration = max_iteration

    def set_data(self, filename: str):
        self.data = np.genfromtxt(filename, delimiter=",")

    def execute_algorithm(self):

        # creating array sampled from normal distribution
        y_values = np.zeros((len(self.data), 2))
        gain = np.ones((len(self.data), 2))
        change = np.zeros((len(self.data), 2))
        for d in range(2):
            for i in range(len(self.data)):
                normal_sample = random.gauss(0, 0.0001)
                y_values[i][d] = normal_sample
        print(y_values)
        print(gain)
        print(change)

        # iterating to max_iteration

        for iteration in range(self.max_iteration):
            # calculating q and Q using the current y_is
            q_values = np.zeros((len(self.data), len(self.data)))
            for i in range(len(self.data)):
                for j in range(len(self.data)): 
                    if i != j:
                        q_values[i][j] = 1/(1 + pow(y_values[i][0] - y_values[j][0], 2) - pow(y_values[i][1] - y_values[j][1], 2))
                    else:
                        q_values[i][j] = 0
                if i == 100:
                    break
            print("q_values is ", q_values)
            break



    def print_data(self):
        print(self.data)


def main():
    tsne = TSNE()
    tsne.set_data("digits.csv")
    tsne.execute_algorithm()

if __name__ == "__main__":
    main()

