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
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.metrics.scorer import make_scorer
from sklearn.metrics import recall_score
import random

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
print(length)
print(len(feature_eventmap_dict))
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
            print(correct_order)
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

#run for 4
km_4 = KMeans(4);
clusters_4 = km_4.fit_predict(x_normalized)
# print(km_4.cluster_centers_)

student_cluster = {}
for index, student in enumerate(student_feature_list):
    if student not in student_cluster:
        if student in grades:
            student_cluster[student] = {
                0: 0, 1: 0, 2: 0, 3: 0, "result": grades[student]}
        else:
            student_cluster[student] = {
                0: 0, 1: 0, 2: 0, 3: 0, "result": None}
    student_cluster[student][clusters_4[index]] += 1

# print(student_cluster)

# high_ach = []
# c0 = []
# c1 = []
# c2 = []
# c3 = []
# c4 = []
# for student in student_cluster:
#     clusters = student_cluster[student]
#     if (clusters["result"] is not None and clusters["result"] >= 0.8
#         and clusters["result"] < 0.9
#         ):
#         high_ach.append(clusters)
#         c0.append(clusters[0])
#         c1.append(clusters[1])
#         c2.append(clusters[2])
#         c3.append(clusters[3])
#         c4.append(clusters[4])
#
# # print(high_ach)
# print(np.array(c0).mean())
# print(np.array(c1).mean())
# print(np.array(c2).mean())
# print(np.array(c3).mean())
# print(np.array(c4).mean())

clf = RandomForestClassifier(random_state=255)
student_features = []
student_label = []
incomplete_students = []
for student in student_cluster:
    clusters = student_cluster[student]
    if clusters["result"] is None:
        incomplete_features = []
        incomplete_features.append(clusters[0])
        incomplete_features.append(clusters[1])
        incomplete_features.append(clusters[2])
        incomplete_features.append(clusters[3])
        incomplete_students.append(incomplete_features)
        continue
    elif clusters["result"] < 0.5:
        # Reduce the massive imbalance of low achieving students
        if random.random() > 0.4:
            student_label.append("Fail")
        else:
            continue
    elif clusters["result"] < 0.65 and clusters["result"] >= 0.5:
        student_label.append("Fail")
    elif clusters["result"] < 0.75 and clusters["result"] >= 0.65:
        student_label.append("Pass")
    elif clusters["result"] >= 0.75:
        student_label.append("Pass")
    cluster_features = []
    cluster_features.append(clusters[0])
    cluster_features.append(clusters[1])
    cluster_features.append(clusters[2])
    cluster_features.append(clusters[3])
    student_features.append(cluster_features)

X_train, X_test, y_train, y_test = train_test_split(
    np.array(student_features), np.array(student_label), test_size=0.25, random_state=255)

print(X_train)
print(y_train)
unique, counts = np.unique(np.array(student_label), return_counts=True)
print(dict(zip(unique, counts)))
clf.fit(X_train, y_train)
predicted = clf.predict(X_test)
print(score(y_test, predicted))

scoring = {'prec_macro': 'precision_macro',
    'rec_micro': make_scorer(recall_score, average='macro')}
scores = cross_validate(clf, np.array(student_features),
    np.array(student_label), scoring=scoring, cv=10, return_train_score=False)
print("Precision: {0}%".format(np.mean(scores['test_prec_macro']) * 100))
print("Recall: {0}%".format(np.mean(scores['test_rec_micro'] * 100)))
print(' ', flush=True)

plot_centroids(np.transpose(km_4.cluster_centers_), correct_order)

# #run silhouette plots on both to determine which is best
# silhouette_plots(x_normalized[0::5],5) #running only on 30000 items as the dataset is too big !
# silhouette_plots(x_normalized[30000:30000+30000],3)
