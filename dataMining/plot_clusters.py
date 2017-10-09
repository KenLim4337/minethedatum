import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pandas as pd
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
    km = KMeans(5);
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

    plt.scatter(x_normalized[clusters == 3, 0],
                x_normalized[clusters == 3, 1],
                s=50, c='lightred',
                marker='v', edgecolor='black',
                label='cluster 4')

    plt.scatter(x_normalized[clusters == 4, 0],
                x_normalized[clusters == 4, 1],
                s=50, c='yellow',
                marker='v', edgecolor='black',
                label='cluster 5')

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