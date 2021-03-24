import numpy as np
from scipy.sparse.linalg import eigs
import matplotlib.pyplot as plt
from sklearn.utils.graph_shortest_path import graph_shortest_path


class Isomap():
    def __init__(self):
        print("Hei")


def isomap(X):
    C = np.genfromtxt('digits_label.csv', delimiter=',')
    C_sorted = np.argsort(C)

    N, D = X.shape

    X2 = np.square(X)
    print(X2)

    v = np.sum(X2, axis=1, keepdims=True)

    print(v)

    D_EU2 = v + v.T - 2 * X @ X.T
    print(D_EU2)
    D_EU = np.sqrt(np.abs(D_EU2))

    if D == 64:
        K = 30
    elif D == 3:
        K = 25

    D_kNN = np.zeros((N, N))

    for i, row in enumerate(D_EU):
        ind = np.argpartition(row, K)[:K] # Index til de K minste elementene
        D_kNN[i][ind] = D_EU[i][ind]

    D_geodesic = graph_shortest_path(D_kNN)
    D_2 = np.square(D_geodesic)
    I = np.identity(N)
    ONE = np.ones(N)
    J = I - ONE @ ONE.T / (N * N)
    B = (-1 / 2) * J @ D_2 @ J
    m = 2
    if D - 1 == m:
        eigenvalues, eigenvectors = np.linalg.eigh(B)
        eigenvalues = eigenvalues[-m:]
        eigenvectors = eigenvectors[:, -m:]
    else:
        eigenvalues, eigenvectors = eigs(B, k=m)

    E_m = eigenvectors
    LAMBDA = np.diag(eigenvalues)

    Y = E_m @ np.sqrt(LAMBDA)
    if D == 64:
        plt.scatter(-Y[:, 0], Y[:, 1], c=C, s=10, marker='.', cmap='jet')
        plt.ylim(-100, 100)
    if D == 3:
        plt.scatter(Y[:, 1], Y[:, 0], c=np.arange(N), s=10, marker='.', cmap='jet')
        plt.ylim(-1, 1)
    plt.show()

X = np.genfromtxt('swiss_data.csv', delimiter=',')
isomap(X)

X = np.genfromtxt('digits.csv', delimiter=',') # K = 30
isomap(X)


