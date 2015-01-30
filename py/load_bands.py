import codecs
from pymongo import Connection


def process_quotes():

    global count

    all_quotes = quotes.find()

    for quote in all_quotes:

        items = quote['manifest']

        for item in items:

            token = item['token']

            if token.isalpha():

                if (token in stop_words) or (token.lower() in stop_words):
                    item['band'] = 's'

                else:
                    firsts = mannheim.find({'vollformen': token}).sort('band',1)
                    if firsts.count() > 0:
                        first = firsts[0]
                        item['band'] = first['band']
                        item['lemma'] = first['grundform']
                    else:
                        firsts = mannheim.find({'vollformen': token.lower()}).sort('band',1)
                        if firsts.count() > 0:
                            first = firsts[0]
                            item['band'] = first['band']
                            item['lemma'] = first['grundform']
                        else:
                            item['band'] = 'u'

            else:  # If token contains non-alpha characters
                item['band'] = 'n'

        quotes.save(quote)

        count += 1
        if count % 10000 == 0:
            print(count)

    return


def load_stop_words(stop_file):
    l = []
    f = codecs.open(stop_file, 'r', encoding='utf-8')
    for line in f:
        w = line.replace('\n', '')
        l.append(w)
    return l


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
    mannheim = db['mannheim']
    quotes = db['quotes']

    stop_words = load_stop_words('Data/stop.txt')
    count = 0
    print("Processing all quotes...")
    process_quotes()

    print("Valmis!")
