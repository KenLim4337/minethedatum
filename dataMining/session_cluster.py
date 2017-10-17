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

cursor = db.sessions.find({"session_duration":{"$gt":0.0}},{"_id":0,"userid":0})
length = db.sessions.count();
if (length == 0):
    raise ValueError('Collection used has no entries. \
        Perhaps you don\'t have the correct collection')
print(length)
print(len(feature_eventmap_dict))
feature_matrix = np.zeros(shape=(length,len(feature_eventmap_dict)))#np.empty((length,len(feature_eventmap_dict)+1), float)
#print(feature_matrix)
count =0

correct_order = None

for document in cursor:
    events_dict = document["events"]
    events_dict["session_duration"] = document["session_duration"]
    if correct_order is None:
        correct_order = list(events_dict)
        print(correct_order)
    #print(np.array(events_dict.values()))
    # print(document)
    # print(list(events_dict))
    '''
    Python3 vs Python2
    '''
    feature_matrix[count,:]=np.array(list(events_dict.values()))
    # feature_matrix[count,:]=np.array(events_dict.values())
    #np.vstack((feature_matrix,np.array(events_dict.values())))
    count = count+1
    # if(count == 10):
    #     break

# print(feature_matrix)
#define the number of clusters to find

min_max_scaler = preprocessing.MinMaxScaler();
#fails because its a dictonary ?
x_normalized = min_max_scaler.fit_transform(feature_matrix);
#run elbow method to find possible k
#elbow_method(x_normalized)
#Function to plot the clusters


# run Kmeans for both k = 3, k=4 & k = 5
# discard one later on
# km_3 = KMeans(3);
# clusters_3 = km_3.fit_predict(x_normalized);
#
# plot_k3(x_normalized,clusters_3,km_3.cluster_centers_)
#run for 5
km_5 = KMeans(5);
clusters_5 = km_5.fit_predict(x_normalized)
print(km_5.cluster_centers_)
# plot_k5(x_normalized,clusters_5,km_5.cluster_centers_)

plot_centroids(np.transpose(km_5.cluster_centers_), correct_order)

# #run silhouette plots on both to determine which is best
# silhouette_plots(x_normalized[0:30000],5) running only on 30000 items as the dataset is too big !
# silhouette_plots(x_normalized[30000:30000+30000],3)
