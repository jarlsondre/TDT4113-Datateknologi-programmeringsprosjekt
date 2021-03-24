import numpy as np
from scipy.sparse.linalg import eigs
import matplotlib.pyplot as plt


class PCA:

    def __init__(self):
        self.X_matrix = None
        self.Y_matrix = None

    def fit(self):
        vectors_t = None
        sum_ = self.X_matrix.sum(axis=0)
        my = 1 / len(self.X_matrix) * sum_
        self.X_matrix - my
        cov_matrix = np.cov(self.X_matrix.T)
        dim = cov_matrix.shape[0]
        if dim - 1 > 2:
            [values, vectors] = eigs(cov_matrix, k=2)
            vectors_t = np.transpose(vectors)
        elif dim - 1 == 2:
            [values, vectors] = np.linalg.eigh(cov_matrix)
            vectors_t = vectors[-2:]
        self.transform(vectors_t)

    def transform(self, transformation_matrix):
        lst = []
        print(transformation_matrix.shape)
        for i in range(len(self.X_matrix)):
            tmp = np.matmul(transformation_matrix, self.X_matrix[i])
            lst.append(tmp)
        self.Y_matrix = np.array(lst)

    def show_result(self):
        if self.Y_matrix.shape[0] == 5620:
            C = np.genfromtxt("digits_label.csv", delimiter=',')
            plt.scatter(self.Y_matrix[:, [0]], self.Y_matrix[:, [1]], s=10, c=C, cmap='jet', marker='.')
        else:
            # Legge på farge?
            plt.scatter(self.Y_matrix[:, [0]], self.Y_matrix[:, [1]], s=10, cmap='jet', marker='.')
        plt.show()

    def read_from_file(self, fil_navn):
        self.X_matrix = np.genfromtxt(fil_navn, delimiter=',')

if __name__ == "__main__":
    pca = PCA()
    pca.read_from_file("swiss_data.csv")
    pca.fit()
    pca.show_result()

    # pca.read_from_file("digits.csv")
    # pca.fit()
    # pca.show_result()

# test
# array = np.array([[1, 2, 3, 4], [1, 2, 3, 4]])
# print(array.shape)
