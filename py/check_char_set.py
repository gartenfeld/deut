from pymongo import Connection
import sys


def connect_to_db(database, collection):

    try:
        db_connection = Connection(host="localhost", port=27017)
        print("Connected to MongoDB successfully!")
        db = db_connection[database]
        handle = db[collection]
    except:
        print("Could not connect to MongoDB.")
    return handle


def inspect_doc(d):

    global excluded
    sentence = d['text']
    if any((c in odd) for c in sentence):
        excluded += 1

    return


def check_collection(c):

    print("Iterating through all documents...")

    all_docs = c.find()

    for doc in all_docs:
        try:
            inspect_doc(doc)
        except:
            print("Error", doc, sys.exc_info())
            continue

    return


if __name__ == '__main__':

    db_name = "deutsch"
    collection_name = "quotes"

    print("Connecting to database...")
    collection = connect_to_db(db_name, collection_name)

    excluded = 0
    odd = ['/', '[', ']', '{', '}', '_', '`', '*', '+', '<', '=', '>', '#', '@', '|', '~', '©', '½']
    check_collection(collection)
    print(str(excluded))

    print("Valmis!")
