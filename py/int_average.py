from pymongo import Connection


def convert_records():

    records = quotes.find()

    for record in records:
        average = record['average']
        record['average'] = float(average)
        quotes.save(record)

    return


def connect_to_db(database):
    try:
        db_connection = Connection(host="localhost", port=27017)
        print("Connected to MongoDB successfully!")
        handle = db_connection[database]
    except:
        print("Could not connect to MongoDB.")
    return handle


if __name__ == "__main__":

    db_name = "deutsch"

    print("Connecting to database...")
    db = connect_to_db(db_name)
    quotes = db['quotes']

    print("Converting...")
    convert_records()

    print("Valmis!")
