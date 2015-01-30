from pymongo import Connection


def export_data():

    records = quotes.find({'richness': {'$gt': 79}})

    for record in records:

        richness = record['richness']
        text = record['text']
        manifest = record['manifest']

        t = {}
        t['richness'] = richness
        t['text'] = text
        t['manifest'] = manifest

        target.insert(t)

    return


def connect_to_db():
    try:
        db_connection = Connection(host="localhost", port=27017)
        print("Connected to MongoDB successfully!")
    except:
        print("Could not connect to MongoDB.")
    return db_connection


if __name__ == "__main__":

    print("Connecting to database...")
    db_conn = connect_to_db()
    deutsch = db_conn['deutsch']
    daten = db_conn['daten']

    quotes = deutsch['quotes']
    target = daten['quotes']

    print("Exporting...")
    export_data()

    print("Valmis!")
