from pymongo import Connection


def run_stats():

    records = quotes.find()

    c = 0

    for record in records:

        text = record['text']
        score = 0

        # Check completeness
        has_cap = text[:1] in caps
        has_final = text[-1:] in finals
        has_odd = any((c in odd) for c in text)
        has_symbols = any((x in symbols) for x in text)

        if has_cap:
            score += 50

        if has_final:
            score += 50

        if has_odd:
            score -= 50

        if has_symbols:
            score -= 25

        # Calculate token scores
        a = record['manifest']

        for t in a:
            band = t['band']

            if band in ['n', 's', 'u']:
                if band == 'n':
                    score -= 2
                if band == 's':
                    score -= 0
                if band == 'u':
                    score -= 2
            else:
                band = int(band)
                if band > 5 and band < 9:
                    score += 1
                if band >= 9 and band < 11:
                    score += 3
                if band >= 11 and band < 13:
                    score += 7
                if band >= 13 and band < 15:
                    score += 5
                if band > 22:
                    score -= 1

        record['richness'] = score

        quotes.save(record)

        c += 1
        if c % 50000 == 0:
            print(c)

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

    caps = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'Ä', 'Ö', 'Ü']
    finals = ['!', '.', '?']
    odd = ['/', '[', ']', '{', '}', '_', '`', '*', '+', '<', '=', '>', '#', '@', '|', '~', '©', '½']
    symbols = ['"', "'", '&', '(', ')', '-', '°', '$', '%']

    print("Converting...")
    run_stats()

    print("Valmis!")
