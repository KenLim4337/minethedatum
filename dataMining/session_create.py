# Event classification method from support code
def event_classification(document):
    classification = None
    feature_eventmap_dict = {'forumread': '/discussion/forum/',
                             'forumcommentread': '/discussion/comments/',
                             'forumsearch': 'discussion/forum/search',
                             'forumcreate': 'forum.thread.created',
                             'videoplay': 'play_video',
                             'videopause': 'pause_video',
                             'videostop': 'stop_video',
                             'videoseek': 'seek_video',
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

    # Initial classification using the event type
    for key in feature_eventmap_dict:
        if  feature_eventmap_dict[key] in document['event_type']:
            classification = key
            break

    # Further classification using the data in document['event']
    event = document['event']
    if classification == 'seek_video' and ('old_time' in event and 'new_time' in event):
        if event['new_time'] > event['old_time']:
            # Set the event classification as a forward seek if the new time is greater than the old time
            classification = 'videoseek_forward'
        else:
            # Else set as backward seek
            classification = 'videoseek_backward'

    return classification

# Just printing stuff for now
def report_session(userid, events_in_session):
    print('----------------------------------------')
    print(userid)
    print(events_in_session)
    session_length = events_in_session[len(events_in_session)-1][0] - events_in_session[0][0]
    print(session_length)


from pymongo import MongoClient
from dateutil import parser
from datetime import timedelta
import json

# Setup connection to DB
client = MongoClient()
dbname = 'think101x2016'
db = client[dbname]

# Initialise collection "session" to store the session data to mongodb
if 'session' not in db.collection_names():
    db.create_collection('session')

cursor = db.clickstream.find()
cnt = 1

# Aggregate events into userid
student_event_map = {}
for document in cursor:
    #print document;
    #Retrieve event classification from event_type field
    event_type = event_classification(document)

    if event_type:
        userid = document['context']['user_id']

        if userid not in student_event_map:
            student_event_map[userid] = []

        student_event_map[userid].append((parser.parse(document['time']), event_type))

        # only read 1000 events for testing
        cnt += 1
        if cnt == 1000:
            break


# Set session threshold as 40 minutes
new_session_threshold = timedelta(minutes=40)

# For each userid,ipaddr
for key in student_event_map.keys():
    userid = key

    # Sort the events in ascending order of time
    student_event_map[key].sort()

    # Initialise a list to contain the events in each session
    events_in_session = [student_event_map[key][0]]
    for i in range(1, len(student_event_map[key])):
        t_diff = student_event_map[key][i][0] - student_event_map[key][i - 1][0]
        if t_diff < new_session_threshold:
            # Append to the current session if the delta between the events is less than the threshold
            events_in_session.append(student_event_map[key][i])
        else:
            # Report the events in the current session list as a separate session, continue with a new list of events
            report_session(userid, events_in_session)
            events_in_session = [student_event_map[key][i]]
