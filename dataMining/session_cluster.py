import sys
import json

from pymongo import MongoClient
from dateutil import parser
from datetime import timedelta
from sklearn.manifold import TSNE
from sklearn import preprocessing
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
from SilhouettePlots import silhouette_plots
from ElbowMethod import elbow_method
from plot_clusters import plot_k3,plot_k5,plot_centroids
from FP_Growth import *
from fp_growth import find_frequent_itemsets





# Setup connection to DB
client = MongoClient()
dbname = 'think101x2016'
db = client[dbname]

feature_eventmap_dict = {
        'forumread': '/discussion/forum/',
        'forumcommentread': '/discussion/comments/',
        'forumsearch': 'discussion/forum/search',
        'forumcreate': 'forum.thread.created',
        'videoplay': 'play_video',
        'videopause': 'pause_video',
        'videostop': 'stop_video',
        'videoseek_forward': "video_seek_forwards",
        'videoseek_backward':"video_seek_backwards",
        'videospeedchange': 'speed_change_video',
        'videoload': 'load_video',
        'checkprogress': 'progress',
        'transcripthide': 'hide_transcript',
        'transcriptshow': 'show_transcript',
        'pageclose': 'page_close',
        'problemgraded': 'problem_grade',
        'problemcheck': 'problem_check',
        'problemsave': 'problem_save',
        'problemshow': 'problem_show',
        'sessionduration': 'session_duration'
}

cursor = db.sessions.find(
    {
        "session_duration":{"$gt" : 0.0},
        "userid" : {"$ne" : ""},
        "userid" : {"$ne" : "null"}
    },
    {"_id" : 0}
)

results = db.results.find()
# Check that the collection we require is present and there are no issues
if (results.count == 0):
    raise ValueError('Results collection has no entries. ' +
        'Perhaps you don\'t have the correct collection')

# Prepare a dictionary of the grade each student received
grades = {}
for grade in results:
    grades[grade["user_id"]] = grade["percent_grade"]

length = cursor.count();
# Check that the collection we require is present and there are no issues
if (length == 0):
    raise ValueError('Sessions collection has no entries. ' +
        'Perhaps you don\'t have the correct collection')
# print(length)
# print(len(feature_eventmap_dict))
feature_matrix = np.zeros(shape=(length,len(feature_eventmap_dict)))#np.empty((length,len(feature_eventmap_dict)+1), float)
#print(feature_matrix)
count =0

correct_order = None
student_feature_list = []

for document in cursor:
    if document["userid"]:
        events_dict = document["events"]
        events_dict["session_duration"] = document["session_duration"]
        if correct_order is None:
            correct_order = list(events_dict)
            #print(correct_order)
        #print(np.array(events_dict.values()))
        # print(document)
        # print(list(events_dict))
        '''
        Python3 vs Python2
        '''
        feature_matrix[count,:]=np.array(list(events_dict.values()))
        student_feature_list.append(document["userid"])
        # feature_matrix[count,:]=np.array(events_dict.values())
        #np.vstack((feature_matrix,np.array(events_dict.values())))
        count = count+1
        # if(count == 10):
        #     break
    else:
        # do nothing
        continue

# print(len(student_feature_list))
feature_matrix = feature_matrix[~np.all(feature_matrix == 0, axis=1)]
# print(len(feature_matrix))
#define the number of clusters to find

min_max_scaler = preprocessing.MinMaxScaler();
#fails because its a dictonary ?
x_normalized = min_max_scaler.fit_transform(feature_matrix);
#run elbow method to find possible k
# elbow_method(x_normalized)
#Function to plot the clusters


# run Kmeans for both k = 3, k=4 & k = 5
# discard one later on
# km_3 = KMeans(3);
# clusters_3 = km_3.fit_predict(x_normalized);
#
# plot_k3(x_normalized,clusters_3,km_3.cluster_centers_)
#run for 5
# km_5 = KMeans(5);
# clusters_5 = km_5.fit_predict(x_normalized)
# print(km_5.cluster_centers_)
# plot_k5(x_normalized,clusters_5,km_5.cluster_centers_)

#run for 4
km_4 = KMeans(4);
clusters_4 = km_4.fit_predict(x_normalized)

# print(len(clusters_5))
# print(len(clusters_4))

student_cluster = {}
#student_cluster_ordered_list dictionary containing a dictionary of a grade and clusters for each student
#In the inner dictionary the clusters is an ordered list of clusters for that student in time
student_cluster_ordered_list = {}
for index, student in enumerate(student_feature_list):
    if student not in student_cluster:
        if student in grades:
            student_cluster[student] = {
                0: 0, 1: 0, 2: 0, 3: 0, 4: 0, "result": grades[student]}
            student_cluster_ordered_list[student] = {"result":grades[student],"clusters":[]}

        else:
            student_cluster[student] = {
                0: 0, 1: 0, 2: 0, 3: 0, 4: 0, "result": None}
            student_cluster_ordered_list[student]={"result":None,"clusters":[]}
    student_cluster[student][clusters_4[index]] += 1
    student_cluster_ordered_list[student]["clusters"].append(clusters_4[index])

# print(student_cluster)
# print(student_cluster_ordered_list)
high_ach = []
high_ach_ordered_list =[]
for student in student_cluster:
    clusters = student_cluster[student]
    clusters_ordered_list = student_cluster_ordered_list[student]
    if clusters["result"] is not None and clusters["result"] >= 0.8:
        high_ach.append(clusters)
        high_ach_ordered_list.append(clusters_ordered_list)
#print(high_ach)
#print(len(high_ach_ordered_list))

plot_centroids(np.transpose(km_4.cluster_centers_), correct_order)

# # #build FP_Tree the min_sup that works is 50% which is way too low
cluster_list = [item['clusters'] for item in high_ach_ordered_list]
# root = FPtree_construction(cluster_list,0.50)
#print(cluster_list)
patterns = find_frequent_itemsets(cluster_list,2000,include_support= True )

for items in patterns:
    print items




# plot_centroids(np.transpose(km_5.cluster_centers_), correct_order)


# #run silhouette plots on both to determine which is best
# silhouette_plots(x_normalized[0::5],5) #running only on 30000 items as the dataset is too big !
# silhouette_plots(x_normalized[30000:30000+30000],3)
