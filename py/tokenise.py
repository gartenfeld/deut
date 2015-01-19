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

    sentence = d['text']
    manifest = make_manifest(sentence)
    # stitch = rebuild(manifest)
    # identical = (sentence == stitch)
    d['manifest'] = manifest
    collection.save(d)

    return


def check_collection(c):

    print("Iterating through all documents...")
    all_docs = c.find()
    for doc in all_docs:
        inspect_doc(doc)

    return


def section(remainder, c):

    n = 0
    while (remainder[n] not in intervening) and (n < len(remainder)-1):
        n += 1
    l = remainder[:n]
    p = remainder[n]
    c.append(l)
    c.append(p)
    r = remainder[n+1:]
    if r != '':
        section(r, c)

    return


def sequence(c):
    a = []
    for idx, item in enumerate(c):
        d = {}
        order = idx+1
        token = item
        d['order'] = order
        d['token'] = token
        a.append(d)
    return a


def make_manifest(t):
    components = []
    section(t, components)
    return sequence(components)


def rebuild(m):
    ordered = sorted(m, key=lambda k: k['order'])
    s = ''
    for item in ordered:
        s = s + item['token']
    return s


if __name__ == '__main__':

    db_name = "deutsch"
    collection_name = "quotes"

    print("Connecting to database...")
    collection = connect_to_db(db_name, collection_name)
    intervening = [' ', '.', '!', '?', ',', ':', ';', '"']

    check_collection(collection)

    print("Valmis!")
