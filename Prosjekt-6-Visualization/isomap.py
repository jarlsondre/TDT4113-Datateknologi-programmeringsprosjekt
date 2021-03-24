"""Isomap"""

import numpy as np
from scipy.sparse.linalg import eigs
import matplotlib.pyplot as plt
import sklearn.utils.graph_shortest_path as sklearn


# N = rows
# D = dim
# D2 = data_2
# v = vector
# D_EU2 = euclidean_distances_2
# D_EU = euclidean_distances
# K = k_smallest
# J = centering_matrix
# B = centered
# Y = mds

class Isomap:
    """Klasse for å ta inn data fra swiss_data og digits og ta de ned til 2D"""

    @staticmethod
    def geodesic_distance(data):
        """Finner geodesic_distance """
        rows, dim = data.shape
        data_2 = np.square(data)
        vector = np.sum(data_2, axis=1, keepdims=True)
        euclidean_distances_2 = vector + vector.T - 2 * data @ data.T
        euclidean_distances = np.sqrt(np.abs(euclidean_distances_2))
        if dim == 64:
            k_smallest = 30
        else:  # dim == 3:
            k_smallest = 25
        d_knn = np.zeros((rows, rows))
        for i, row in enumerate(euclidean_distances):
            ind = np.argpartition(row, k_smallest)[:k_smallest]  # Index til de K minste elementene
            d_knn[i][ind] = euclidean_distances[i][ind]
        d_geodesic = sklearn.graph_shortest_path(d_knn)
        return d_geodesic

    @staticmethod
    def multidimensional_scaling(d_geo, dim):
        """Utfører multidimensional_scaling"""
        rows = d_geo.shape[0]
        d_2 = np.square(d_geo)
        identity = np.identity(rows)
        one = np.ones(rows)
        centering_matrix = identity - one @ one.T / (rows * rows)
        centered = (-1 / 2) * centering_matrix @ d_2 @ centering_matrix
        m_m = 2
        if dim - 1 == m_m:
            eigenvalues, eigenvectors = np.linalg.eigh(centered)
            eigenvalues = eigenvalues[-m_m:]
            eigenvectors = eigenvectors[:, -m_m:]
        else:
            eigenvalues, eigenvectors = eigs(centered, k=m_m)

        e_m = eigenvectors
        lam = np.diag(eigenvalues)
        return e_m @ np.sqrt(lam)

    @staticmethod
    def show(mds, dim):
        """Plotter"""
        rows = mds.shape[0]
        if dim == 64:
            color = np.genfromtxt('digits_label.csv', delimiter=',')
            plt.scatter(-mds[:, 0], mds[:, 1], c=color, s=10, marker='.', cmap='jet')
            plt.ylim(-100, 100)
        if dim == 3:
            color = np.arange(rows)
            plt.scatter(mds[:, 1], mds[:, 0], c=color, s=10, marker='.', cmap='jet')
            plt.ylim(-1, 1)
        plt.show()

    def swiss(self):
        """Tar inn fra swiss_data, regner ut og plotter"""
        data = np.genfromtxt('swiss_data.csv', delimiter=',')
        d_geo = self.geodesic_distance(data)
        mds = self.multidimensional_scaling(d_geo, dim=3)
        self.show(mds, dim=3)

    def digits(self):
        """Tar inn fra digits, regner ut og plotter"""
        data = np.genfromtxt('digits.csv', delimiter=',')
        d_geo = self.geodesic_distance(data)
        mds = self.multidimensional_scaling(d_geo, dim=64)
        self.show(mds, dim=64)


isomap = Isomap()
isomap.swiss()
isomap.digits()
