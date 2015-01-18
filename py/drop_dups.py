from pymongo import Connection


def connect_to_db(database, collection):

    try:
        db_connection = Connection(host="localhost", port=27017)
        print("Connected to MongoDB successfully!")
        db = db_connection[database]
        handle = db[collection]
    except:
        print("Could not connect to MongoDB.")
    return handle


def drop_dups(c):

    print("Aggregating Documents...")

    dup_sets = c.aggregate([
        { "$group": 
            {     "_id": { "text" : "$text"},
            "uniqueIds": { "$addToSet": "$_id" },
                "count": { "$sum": 1 } } 
        }, 
        { "$match": 
            {   "count": { "$gt": 1 } } 
        }
    ], cursor={}, allowDiskUse=True)

    deleted_count = 0

    print("Dropping duplicates...")
    for doc in dup_sets:  # All duplicate groups with count > 1
        dups = doc["uniqueIds"]  # Get the array of IDs within each dup group
        for i, doc_id in enumerate(dups):
            if i > 0:  # After the first instance
                dup_doc = c.find_one({"_id": doc_id})  # Grab document by _id
                c.remove(dup_doc)  # Delete document
                deleted_count += 1
                # print("#" + str(i+1), dup_doc["text"][:10] + "... removed.")
    print(str(deleted_count) + " duplicates deleted.")
    return

if __name__ == '__main__':

    db_name = "deutsch"
    collection_name = "quotes"

    print("Connecting to database...")
    collection = connect_to_db(db_name, collection_name)

    drop_dups(collection)

    print("Valmis!")
