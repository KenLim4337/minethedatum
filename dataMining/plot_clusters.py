import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
def plot_k3(x_normalized, clusters, cluster_centers):
    km = KMeans(3);
    plt.scatter(x_normalized[clusters == 0, 0],
                x_normalized[clusters == 0, 1],
                s=50, c='lightgreen',
                marker='s', edgecolor='black',
                label='cluster 1')

    plt.scatter(x_normalized[clusters == 1, 0],
                x_normalized[clusters == 1, 1],
                s=50, c='orange',
                marker='o', edgecolor='black',
                label='cluster 2')
    plt.scatter(x_normalized[clusters == 2, 0],
                x_normalized[clusters == 2, 1],
                s=50, c='lightblue',
                marker='v', edgecolor='black',
                label='cluster 3')
    plt.scatter(cluster_centers[:, 0],
                cluster_centers[:, 1],
                s=250, marker='*',
                c='red', edgecolor='black',
                label='centroids')
    plt.legend(scatterpoints=1)
    plt.grid()
    plt.tight_layout()
    # plt.savefig('images/11_02.png', dpi=300)
    plt.show()


def plot_k5(x_normalized, clusters, cluster_centers):
    print(cluster_centers)
    plt.scatter(x_normalized[clusters == 0, 0],
                x_normalized[clusters == 0, 1],
                s=50, c='g',
                marker='s', edgecolor='black',
                label='cluster 1')

    plt.scatter(x_normalized[clusters == 1, 0],
                x_normalized[clusters == 1, 1],
                s=50, c='m',
                marker='o', edgecolor='black',
                label='cluster 2')

    plt.scatter(x_normalized[clusters == 2, 0],
                x_normalized[clusters == 2, 1],
                s=50, c='b',
                marker='v', edgecolor='black',
                label='cluster 3')

    plt.scatter(x_normalized[clusters == 3, 0],
                x_normalized[clusters == 3, 1],
                s=50, c='r',
                marker='.', edgecolor='black',
                label='cluster 4')

    plt.scatter(x_normalized[clusters == 4, 0],
                x_normalized[clusters == 4, 1],
                s=50, c='yellow',
                marker='^', edgecolor='black',
                label='cluster 5')

    plt.scatter(cluster_centers[:, 0],
                cluster_centers[:, 1],
                s=250, marker='*',
                c='y', edgecolor='black',
                label='centroids')

    plt.legend(scatterpoints=1)
    plt.grid()
    plt.tight_layout()
    # plt.savefig('images/11_02.png', dpi=300)
    plt.show()


def plot_centroids(cluster_centers, labels):
    plt.plot(np.arange(0, 20), cluster_centers[:, 0], label = 'Cluster 1')
    plt.plot(np.arange(0, 20), cluster_centers[:, 1], label = 'Cluster 2')
    plt.plot(np.arange(0, 20), cluster_centers[:, 2], label = 'Cluster 3')
    plt.plot(np.arange(0, 20), cluster_centers[:, 3], label = 'Cluster 4')
    plt.plot(np.arange(0, 20), cluster_centers[:, 4], label = 'Cluster 5')
    plt.legend()
    plt.grid()
    plt.xticks(np.arange(0, 20), labels, rotation=70)
    plt.tight_layout()
    # plt.savefig('images/11_02.png', dpi=300)
    plt.show()
