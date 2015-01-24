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

    a = l.rstrip().split('\t')

    # If a column is missing...
    if len(a) is not 2:
        raise IndexError

    raw_form = a[0]
    immediate = a[1]

    # To deal with odd entries, e.g. '?'
    if not immediate.isalpha() and '-' not in immediate:
        immediate = raw_form

    # Create dictionary object
    record = {
        "vollform": raw_form,
        "immediate": immediate
        }

    # Insert document into DB
    collection.insert(record, safe=True)


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

    source_file = "Data/morphy.txt"
    db_name = "deutsch"
    collection_name = "morphy"

    print("Connecting to database...")
    collection = connect_to_db(db_name, collection_name)

    print("Processing file...")
    process_file(source_file)

    print("Valmis!")
