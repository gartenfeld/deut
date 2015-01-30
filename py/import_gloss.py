from pymongo import Connection


def load_gloss():

    records = quotes.find()

    for record in records:

        a = record['manifest']

        for t in a:

            band = t['band']
            if band not in ['n', 's']:
                if band == 'u':
                    lemma = t['token']
                else:
                    lemma = t['lemma']
                # Try find a gloss for the token
                entry = richter.find_one({'de': lemma})
                if entry != None:
                    gloss = entry['en']
                    t['gloss'] = gloss
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
    richter = db['richter']

    print("Loading gloss...")
    load_gloss()

    print("Valmis!")
