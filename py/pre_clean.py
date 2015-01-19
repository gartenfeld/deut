from pymongo import Connection
import sys
import re

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

    s = d['text']

    # Asterisk => ''
    s = re.sub(r'\*', '', s)
    # Double space => space
    s = re.sub(r' +', ' ', s)
    # '( ' => '(', ' )' => ')'
    s = re.sub(r'\( ', '(', s)
    s = re.sub(r' \)', ')', s)
    # Initial '- ' => ''
    if s[:2] == '- ':
        s = s[2:]
    # Trailing colon, semicolon => ...
    if s[-1:] in [':', ';', ',']:
        s = s[:-1] + '...'
    # Space punct => punct
    for punct in ['.', '!', '?', ',', ':', ';']:
        pattern = re.compile((' \\' + punct))
        s = re.sub(pattern, punct, s)
    # Space apostrophe space => apostrophe space
    s = re.sub(r' \' ', '\'', s)
    # 'z ` B.' => 'z. B.'
    s = re.sub(r'z ` B\.', 'z\. B\.', s)
    # Strip sentence
    s = s.strip()

    if s != d['text']:
        d['text'] = s
        collection.save(d)

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

    check_collection(collection)

    print("Valmis!")
