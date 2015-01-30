import re
import sys
import codecs
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


def unpack_line(l):

    # Separate German and English
    a = l.split('::')

    if len(a) == 2:
        de = a[0].strip()
        en = a[1].strip()

        # Separate DE array
        de_first = de.split('|')[0]
        de_first = re.sub(r'\[.*\]', '', de_first)
        de_first = re.sub(r'\{.*\}', '', de_first)
        de_first = re.sub(r'\(.*\)', '', de_first)
        de_first = re.sub(r'\/.*\/', '', de_first)
        de_first = de_first.split(';')[0]
        de_first = re.sub(r' +', ' ', de_first)
        de_first = de_first.strip()

        if de_first not in d:
            d.append(de_first)

            en_first = en.split('|')[0]
            en_first = re.sub(r'\[.*\]', '', en_first)
            en_first = re.sub(r'\{.*\}', '', en_first)
            en_first = re.sub(r'\/.*\/', '', en_first)
            en_first = re.sub(r'\<.*\>', '', en_first)
            en_first = en_first.split(';')[0]
            en_first = re.sub(r' +', ' ', en_first)
            en_first = en_first.strip()

            record = {}
            record['de'] = de_first
            record['en'] = en_first

            collection.insert(record)


def process_file(data_file):

    f = codecs.open(data_file, 'r', encoding='utf-8')

    for line in f:

        try:
            unpack_line(line)

        except:
            print("Error:\t" + line + '\n')
            print(sys.exc_info())
            continue

    f.close()

    return


if __name__ == "__main__":

    source_file = "Data/richter.txt"
    d = []
    db_name = "deutsch"
    collection_name = "richter"

    print("Connecting to database...")
    collection = connect_to_db(db_name, collection_name)

    print("Processing file...")
    process_file(source_file)

    print("Valmis!")
