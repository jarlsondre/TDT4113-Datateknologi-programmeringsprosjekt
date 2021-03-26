import numpy as np
import random
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
        # print("euclidean distance", euclidean_distance)

        # creating k-nn-graph
        k_smallest = 25
        knn_graph = np.zeros((rows, rows))
        for i, row in enumerate(euclidean_distance):
            ind = np.argpartition(row, k_smallest)[:k_smallest]
            knn_graph[i][ind] = euclidean_distance[i][ind]
            
        # creating p-graph
        p_graph = (knn_graph + knn_graph.T > 0).astype(float)

        # freeing up the memory 
        del knn_graph
        del euclidean_distance
        del euclidean_distance_squared
        del self.data

        P_graph = p_graph / p_graph.sum()

        random.seed(version=100)


        # creating array sampled from normal distribution
        y_values = np.zeros((rows, 2))
        gain = np.ones((rows, 2))
        change = np.zeros((rows, 2))
        for d in range(2):
            for i in range(rows):
                y_values[i][d] = random.gauss(0, 0.0001)
        

        # iterating to max_iteration

        print("starting iteration")
        for iteration in range(self.max_iteration):

            if iteration > 250:
                alpha = 0.8
            else:
                alpha = 0.5
            epsilon = 500

            # calculating q and Q using the current y_is
            q_values = np.zeros((rows, rows))
            for i in range(rows):
                for j in range(rows): 
                    if i != j:
                        q_values[i][j] = 1/(1 + pow(y_values[i][0] - y_values[j][0], 2) - pow(y_values[i][1] - y_values[j][1], 2))
                    else:
                        q_values[i][j] = 0

            print("q_values is ", q_values)

            Q_values = q_values / q_values.sum()

            G = (P_graph - Q_values) * q_values
            S = np.diag(np.sum(G, axis=1))


            # calculating the gradient over each y_i
            gradient_matrix = 4 * (S - G) @ y_values
            print(gradient_matrix)

            for d in range(2):
                for i in range(rows):
                    if gradient_matrix[i][d]*change[i][d] > 0:
                        gain[i][d] *= 0.8
                    else:
                        gain[i][d] += 0.2
                    change[i] = alpha*change[i] - epsilon*gain[i]*gradient_matrix[i]
            
            print(gain, change)
            break



    def print_data(self):
        print(self.data)


def main():
    tsne = TSNE()
    tsne.set_data("swiss_data.csv")
    tsne.execute_algorithm()

if __name__ == "__main__":
    main()

