import numpy as np
from scipy.sparse.linalg import eigs
import matplotlib.pyplot as plt


class PCA():

    def __init__(self):
        self.X_matrix = None
        self.Y_matrix = None
        self.my = None

    def fit(self):
        sum_ = self.X_matrix.sum(axis=0)
        self.my = 1 / len(self.X_matrix) * sum_
        self.X_matrix - self.my
        # print(self.X_matrix.shape)
        cov_matrix = np.cov(self.X_matrix.T)
        if 64 - 1 > 2: # Bytte ut 64 med dim til Xvalues. Antall kolonner.
            [values, vectors] = eigs(cov_matrix, k=2)

        # Sortere å finne de to støste egenverdiene og tilhørende egenvektorer:
        # elif 3 - 1 == 2:
        #     [values, vectors] = np.linalg.eigh(cov_matrix)[1][-2:]
        # print(vectors.shape)
        vectors_T = np.transpose(vectors)
        self.transform(vectors_T)

    def transform(self, transformation_matrix):
        lst = []
        print(transformation_matrix.shape)
        for i in range(len(self.X_matrix)):
            tmp = np.matmul(transformation_matrix, self.X_matrix[i])
            lst.append(tmp)
        self.Y_matrix = np.array(lst)

    def show_result(self):
        C = np.genfromtxt("digits_label.csv", delimiter=',')
        plt.scatter(self.Y_matrix[:, [0]], self.Y_matrix[:, [1]], s=10, c=C, cmap='jet', marker='.')
        plt.show()

    def read_from_file(self, fil_navn):
        self.X_matrix = np.genfromtxt(fil_navn, delimiter=',')


def main():
    pca = PCA()


if __name__ == "__main__":
    pca = PCA()
    pca.read_from_file("digits.csv")
    # print(pca.X_matrix)
    pca.fit()
    # print(pca.Y_matrix)
    pca.show_result()

# test
# array = np.array([[1, 2, 3, 4], [1, 2, 3, 4]])
# print(array.shape)
