import numpy as np
from FP_Node import FP_Node
"""
items is a list of ordered clusters list from each student i.e
[[0,1,0,0,0,2,3,0,0,1],[0,1,2,3],...,[0,1,3,0,0,0,0,0,0,1,2]]
"""
def FPtree_construction(student_clusters,min_sup):
    #print(student_clusters)
    #general count of clusters
    count =0
    #count dict for each type of cluster
    count_dict = {0: 0, 1: 0, 2: 0, 3: 0}
    for clusters in student_clusters:
        #for each transaction
        for cluster in clusters:
            #get the count of the cluster
            count = count +1
            count_dict[cluster] +=1
    #generate the frequent itemsets
    # print(count)
    # print(count_dict)
    frequent_1itemsets = []
    for cluster in count_dict.keys():
        cluster_sup = float(count_dict[cluster])/count
        print("Cluster: {} Support: {}".format(cluster,cluster_sup))
        if(cluster_sup > min_sup):
            #append the key (cluster) and its sup to the list
            frequent_1itemsets.append((cluster,cluster_sup))
    #sort the list by sup in descending order (wihtout reverse it will be in ascending order)
    frequent_1itemsets.sort(key = sort_by_sup, reverse= True)
    #make sure its correct
    print("Frequend items {} at min_sup {}".format(frequent_1itemsets, min_sup))
    #remove the sups from frequent_1itemsets
    frequent_1itemsets = [items[0] for items in frequent_1itemsets]
    #make sure its correct
    # print(frequent_1itemsets)
    #create root node
    root = FP_Node(None,0,[],None)
    for clusters in student_clusters:
        #Select the frequent items in clusters and sort them according to the order of frequent_1itemsets.
        filtered_clusters = [cluster for cluster in clusters if(frequent_1itemsets.__contains__(cluster))]
        #make sure its correct

        if(len(filtered_clusters)>0):
            root.insert(filtered_clusters)

    return root


def sort_by_sup(item):
    return item[1]








