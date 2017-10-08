import sys
import json

from pymongo import MongoClient
from dateutil import parser
from datetime import timedelta
from sklearn.manifold import TSNE
from sklearn import preprocessing
from sklearn.cluster import KMeans

import bokeh.plotting as bp
from bokeh.plotting import figure, output_notebook, show, ColumnDataSource, output_file
from bokeh.models import HoverTool



# Setup connection to DB
client = MongoClient()
dbname = 'think101x2016'
db = client[dbname]


cursor = db.session.find();
#define the number of clusters to find
min_max_scaler = preprocessing.MinMaxScaler();
#fails because its a dictonary ?
x_normalized = min_max_scaler.fit_transform(cursor);
k = 15
#initialize K-means
km = KMeans(k);
clusters = km.fit_predict(x_normalized);

X_tsne = TSNE(learning_rate=100, n_components=2).fit_transform(x_normalized)

