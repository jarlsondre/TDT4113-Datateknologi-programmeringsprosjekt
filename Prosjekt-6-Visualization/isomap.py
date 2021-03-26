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
    def get_euclidean_distances(data):
        """Tar inn et datasett og returnerer parvis euclidean distance"""
        vector = np.sum(data * data, axis=1, keepdims=True)
        return np.sqrt(np.abs(vector + vector.T - 2 * (data @ data.T)))

    @staticmethod
    def get_geodesic_distance(data, k_smallest):
        """Finner geodesic_distance """
        rows = data.shape[0]
        d_knn = np.zeros((rows, rows))
        # Setter inn de k minste verdiene
        for i, row in enumerate(data):
            ind = np.argpartition(row, k_smallest)[:k_smallest]
            d_knn[i][ind] = data[i][ind]
        return sklearn.graph_shortest_path(d_knn)

    @staticmethod
    def multidimensional_scaling(d_geo, dim):
        """Utfører multidimensional_scaling"""
        rows = d_geo.shape[0]
        d_2 = d_geo * d_geo
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

    @staticmethod
    def swiss():
        """Tar inn fra swiss_data, regner ut og plotter"""
        data = np.genfromtxt('swiss_data.csv', delimiter=',')
        euclidean_distances = Isomap.get_euclidean_distances(data)
        d_geo = Isomap.get_geodesic_distance(euclidean_distances, k_smallest=25)
        mds = Isomap.multidimensional_scaling(d_geo, dim=3)
        Isomap.show(mds, dim=3)

    @staticmethod
    def digits():
        """Tar inn fra digits, regner ut og plotter"""
        data = np.genfromtxt('digits.csv', delimiter=',')
        euclidean_distances = Isomap.get_euclidean_distances(data)
        d_geo = Isomap.get_geodesic_distance(euclidean_distances, k_smallest=30)
        mds = Isomap.multidimensional_scaling(d_geo, dim=64)
        Isomap.show(mds, dim=64)


Isomap.swiss()
Isomap.digits()
