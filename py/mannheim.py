import re
import sys
import codecs
from pymongo import Connection


def unpack_slashes(w):
    m = re.search(r'der\/die\/das([\w]+)', w)
    stem = m.group(1)
    u = 'der' + stem + ',die' + stem + ',das' + stem
    return u


def unpack_brackets(x):
    m = re.search(r'(.+)\((.+)\)', x)
    stem = m.group(1)
    endings = m.group(2).split(',')
    variants = []
    for ending in endings:
        variants.append(stem + ending)
        v = ','.join(variants)
    return v


def unpack_line(l):

    global count

    a = l.rstrip().split(' ')

    literal = a[0]
    freq_band = a[1]
    pos = 'UNSP'  # Default tag

    if len(a) == 3:  # If tag present
        pos = a[2]  # Set to tag provided

    # Unpack slashes
    if '/' in literal:
        literal = unpack_slashes(literal)

    # Unpack brackets
    if '(' in literal:
        literal = unpack_brackets(literal)

    #if isinstance(literal, str): literal = literal.decode('utf-8')

    # Set up the dictionary
    rank = count + 1
    band = freq_band
    wortart = pos
    grundform = literal
    vollformen = []

    # Resolve multiple headwords
    literal_array = literal.split(',')
    # If there are multiple headwords
    if len(literal_array) > 1:

        # Set the default values
        shortest = 100
        grundform = "NOTFOUND"

        # For each headword in the headword array
        for variant in literal_array:

            lookup = morphy.find({"vollform": variant}).limit(1)

            # If 'vollform' can be found
            if lookup.count() > 0:
                # Get the immediate parent
                new_lookup = lookup[0].get("immediate")

                # If the parent is a shorter word
                if len(new_lookup) < shortest:
                    grundform = new_lookup
                    shortest = len(new_lookup)

            # If 'vollform' cannot be found, try find 'grundform'
            elif morphy.find({"immediate": variant}).limit(1).count() > 0:

                if len(variant) < shortest:
                    grundform = variant
                    shortest = len(variant)

            else:
                grundform = variant
                vollformen += literal_array

    vollformen.append(grundform)

    #Search for and add fullforms
    fullforms = morphy.find({"immediate": grundform},{"vollform":1})
    for doc in fullforms:
        form = doc.get("vollform")
        vollformen.append(form)

    # Construct dictionary
    entry = {   "rank" : rank, 
                "band" : band,
             "wortart" : wortart,
           "grundform" : grundform,
          "vollformen" : vollformen }

    # Insert document into DB
    mannheim.insert(entry)
    count += 1

    if count % 10000 == 0:
        print(count)



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


def connect_to_db(database):
    try:
        db_connection = Connection(host="localhost", port=27017)
        print("Connected to MongoDB successfully!")
        handle = db_connection[database]
    except:
        print("Could not connect to MongoDB.")
    return handle


if __name__ == "__main__":

    source_file = "Data/mannheim.txt"
    db_name = "deutsch"

    print("Connecting to database...")
    db = connect_to_db(db_name)
    morphy = db['morphy']
    mannheim = db['mannheim']

    count = 0
    print("Processing Mannheim source file...")
    process_file(source_file)

    print("Valmis!")
