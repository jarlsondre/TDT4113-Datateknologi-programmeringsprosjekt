import numpy as np
from scipy.sparse.linalg import eigs
import matplotlib.pyplot as plt
from sklearn.utils.graph_shortest_path import graph_shortest_path


class Isomap():
    def __init__(self):
        print("Hei")


X = np.genfromtxt('swiss_data.csv', delimiter=',')
X2 = np.square(X)

v = np.sum(X2, axis=1, keepdims=True)


D_EU2 = v + v.T - 2 * X @ X.T
D_EU = np.sqrt(np.absolute(D_EU2))


K = 10
D_kNN = D_EU
for i, row in enumerate(D_kNN):
    sorted_row = sorted(row)
    threshold = sorted_row[K - 1]
    for j, col in enumerate(row):
        if col > threshold and i != j:
            D_kNN[i][j] = 0

D_geodesic = graph_shortest_path(D_kNN)

D_2 = np.square(D_geodesic)

N = len(D_2)
I = np.identity(N)
ONE = np.ones(N)

J = I - 1/N * ONE @ ONE.transpose()

B = -1/2 * J @ D_2 @ J
m = 2
eigenvalues, eigenvectors = np.linalg.eigh(B)
eigenvalues = eigenvalues[-m:]
for i in eigenvectors[-m:]:
    print(i)

# ind = np.argpartition(eigenvalues, -m)[-m:]
#LAM = np.diag(eigenvalues[ind])
#E_m = eigenvectors[:, ind]

E_m = eigenvectors
LAM = np.diag(eigenvalues)



Y = E_m @ np.sqrt(LAM)


plt.scatter(Y[:, 1], Y[:, 0], c=np.arange(N))
plt.show()




