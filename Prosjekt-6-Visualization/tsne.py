import numpy as np
import random
import matplotlib.pyplot as plt
import sys

np.set_printoptions(threshold=100)



class TSNE():

    def __init__(self, max_iteration = 100):
        self.data = None
        self.max_iteration = max_iteration

    def set_data(self, filename: str):
        self.data = np.genfromtxt(filename, delimiter=",")

    def execute_algorithm(self):

        rows, dims = self.data.shape

        # creating distance-matrix
        squared_data = np.square(self.data)
        vector = np.sum(squared_data, axis=1, keepdims=True)
        euclidean_distance_squared = vector + vector.T - 2 * self.data @ self.data.T
        euclidean_distance = np.sqrt(np.abs(euclidean_distance_squared))


     
        # creating k-nn-graph
        k_smallest = 25
        knn_graph = np.zeros((rows, rows))
        for i, row in enumerate(euclidean_distance):
            ind = np.argpartition(row, k_smallest)[:k_smallest]
            knn_graph[i][ind] = euclidean_distance[i][ind]


        # creating p-graph
        p_graph = (knn_graph + knn_graph.T > 0).astype(float)
        P_graph = p_graph / np.sum(p_graph)

        random.seed(version=100)

        # creating array sampled from normal distribution

        y = np.random.randn(knn_graph.shape[1], 2) * 1e-4
        y_values = np.zeros((rows, 2))
        gain = np.ones((rows, 2))
        change = np.zeros((rows, 2))
        for d in range(2):
            for i in range(rows):
                y_values[i][d] = random.gauss(0, 0.0001)

        y_values = np.random.randn(knn_graph.shape[1], 2) * 1e-4
        print(f"y-values are initially: {y_values}")
        print(f"y is {y}")

        

        # iterating to max_iteration

        for iteration in range(200):
            print("starting iteration", iteration)
            alpha = 0.8 if iteration > 250 else 0.5
            epsilon = 500

            vector = np.sum(y_values**2, axis=1, keepdims=True)

            # calculating q and Q using the current y_is
            q_values = 1 / (1 + (vector + vector.T - 2 * (y_values @ y_values.T)))

            Q_values = q_values / np.sum(q_values)

            G = 4 * (P_graph - Q_values) * q_values
            S = np.diag(np.sum(G, axis=1))

            # calculating the gradient over each y_i
            gradient_matrix = 4 * (S - G) @ y_values

            # updating the gain and the change
            gain[np.sign(gradient_matrix) == np.sign(change)] *= 0.8
            gain[np.sign(gradient_matrix) != np.sign(change)] += 0.2
            gain[gain < 0.01] = 0.01

            change = (alpha*change) - (epsilon*gain*gradient_matrix)
            y_values += change

        # Showing the plot
        color = np.genfromtxt('digits_label.csv', delimiter=",")
        plt.scatter(y_values[:, 0], y_values[:, 1], c=color, s=10, marker=".", cmap="jet")
        plt.show()



    def print_data(self):
        print(self.data)


def main():
    tsne = TSNE()
    tsne.set_data("digits.csv")
    tsne.execute_algorithm()

if __name__ == "__main__":
    main()

