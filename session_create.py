# Event classification method from support code
def event_classification(event):
    classification = None
    feature_eventmap_dict = {'forumread': '/discussion/forum/', 'forumcommentread': '/discussion/comments/',
                             'videoplay': 'play_video', 'videopause': 'pause_video', 'videostop': 'stop_video',
                             'videoseek': 'seek_video', 'videospeedchange': 'speed_change_video',
                             'forumsearch': 'discussion/forum/search', 'checkprogress': 'progress',
                             'videoload': 'load_video'
                            }
    for key in feature_eventmap_dict:
        if  feature_eventmap_dict[key] in event:
            classification = key
            break
    return classification

# Just printing stuff for now
def report_session(userid, ipaddr, events_in_session):
    print('----------------------------------------')
    print(userid)
    print(ipaddr)
    print(events_in_session)
    print(events_in_session[len(events_in_session)-1][0] - events_in_session[0][0])



from pymongo import MongoClient
from dateutil import parser
from datetime import timedelta
import json

# Setup connection to DB
client = MongoClient()
dbname = 'think101x2016'
db = client[dbname]

"""
if 'session' not in db.collection_names():
    db.create_collection('session')
"""

cursor = db.clickstream.find()
cnt = 1

# Aggregate events into userid,ipaddr
thing = {}
for document in cursor:
    event_type = event_classification(document['event_type'])
    if event_type:
        userid = document['context']['user_id']
        ipaddr = document['ip']

        if ( userid,ipaddr ) not in thing:
            thing[userid,ipaddr] = []

        thing[userid,ipaddr].append(( parser.parse(document['time']),event_type ))

        # only read 1000 events for testing
        cnt += 1
        if cnt == 1000:
            break


# Set threshold as 1 hour
new_session_threshold = timedelta(hours=1)

# For each userid,ipaddr
for key in thing.keys():
    userid,ipaddr = key

    # Sort the events in ascending order of time
    thing[key].sort()

    # Initialise a list to contain the events in each session
    events_in_session = [ thing[key][0] ]
    for i in range(1, len(thing[key])):
        t_diff = thing[key][i][0] - thing[key][i-1][0]
        if t_diff < new_session_threshold:
            # Append to the current session if the delta between the events is less than the threshold
            events_in_session.append(thing[key][i])
        else:
            # Report the events in the current session list as a separate session, continue with a new list of events
            report_session(userid, ipaddr, events_in_session)
            events_in_session = [ thing[key][i] ]
