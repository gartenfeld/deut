from pymongo import Connection


def run_stats():

    records = quotes.find()

    for record in records:

        # Check completeness
        text = record['text']
        has_cap = text[:1] in caps
        has_final = text[-1:] in finals
        has_odd = any((c in odd) for c in text)

        if has_cap and has_final and (not has_odd):
            record['complete'] = 1
        else:
            record['complete'] = 0

        # Calculate length
        record['length'] = len(text)

        # Calculate average
        a = record['manifest']
        total = 0
        denom = 0
        for t in a:
            band = t['band']
            if band not in ['u', 'n', 's']:
                total += int(band)
                denom += 1
        if denom > 0:
            average = total / denom
            average = "%.2f" % average
        else:
            average = 30
        record['average'] = average

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

    caps = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'Ä', 'Ö', 'Ü']
    finals = ['!', '.', '?']
    odd = ['/', '[', ']', '{', '}', '_', '`', '*', '+', '<', '=', '>', '#', '@', '|', '~', '©', '½']

    print("Converting...")
    run_stats()

    print("Valmis!")
