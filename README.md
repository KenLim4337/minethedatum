From the main data source (clickstream) extract a new collection called reducedClickstream of only the required fields.


db.clickstream.aggregate([
    { $match : {
        "context.user_id" : { $ne : null }
    }},
    { $project : {
        "context.user_id" : 1,
        event_type : 1,
        time : 1,
        event : 1
    }},
    { $sort : { time : 1 } },
    { $out : "reducedClickstream" }
],
{ allowDiskUse : true }).pretty()


Once this collection is added to mongodb, the python script session_create can be run.

This will add a 'sessions' collection to mongo, for further analysis to be performed.

Alternatively add the session.json file to mongo using the following. Which will need to be run from the command line to add the 'session' collection to mongo.
mongoimport -d think101x2016 -c session --type json --file session.json

Further, the following command will need to be run from the command line to add the 'results' collection to mongo.
mongoimport -d think101x2016 -c results --type tsv --file <path-to-file> --headerline

Following this, the session_cluster script can be run to perform the data mining.
