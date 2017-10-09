import sys
import json

from pymongo import MongoClient
from dateutil import parser
from datetime import timedelta
from sklearn.manifold import TSNE
from sklearn import preprocessing
from sklearn.cluster import KMeans
import numpy as np
import bokeh.plotting as bp
from bokeh.plotting import figure, output_notebook, show, ColumnDataSource, output_file
from bokeh.models import HoverTool



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
        'problemshow': 'problem_show'
}

cursor = db.sessions.find({"session_duration":{"$gt":0.0}},{"_id":0,"userid":0})
length = db.sessions.count();
print(length)
print(len(feature_eventmap_dict)+1)
feature_matrix = np.zeros(shape=(length,len(feature_eventmap_dict)+1))#np.empty((length,len(feature_eventmap_dict)+1), float)
#print(feature_matrix)
count =0

for document in cursor:
    events_dict = document["events"]
    events_dict["session_duration"] = document["session_duration"]
    #print(np.array(events_dict.values()))
    feature_matrix[count,:]=np.array(events_dict.values())
    #np.vstack((feature_matrix,np.array(events_dict.values())))
    count = count+1
    # if(count == 10):
    #     break

# print(feature_matrix)
#define the number of clusters to find

min_max_scaler = preprocessing.MinMaxScaler();
#fails because its a dictonary ?
x_normalized = min_max_scaler.fit_transform(feature_matrix);
k = 15
#initialize K-means
km = KMeans(k);
clusters = km.fit_predict(x_normalized);


