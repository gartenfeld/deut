def section(remainder, c):

    n = 0
    while remainder[n] not in intervening:
        n += 1
    l = remainder[:n]
    p = remainder[n]
    c.append(l)
    c.append(p)
    r = remainder[n+1:]
    if r != '':
        section(r, c)

    return


def sequence(c):
    a = []
    for idx, item in enumerate(c):
        d = {}
        order = idx+1
        token = item
        d['order'] = order
        d['token'] = token
        a.append(d)
    return a


def make_manifest(t):
    components = []
    section(t, components)
    return sequence(components)


def rebuild(m):
    ordered = sorted(m, key=lambda k: k['order'])
    s = ''
    for item in ordered:
        s = s + item['token']
    return s

if __name__ == '__main__':

    text = 'Denn sie ist so banal, so aalglatt komponiert, daß man sich vor " Verlegenheit " im bequemen Theatersessel winden möchte.'
    intervening = [' ', '.', '!', '?', ',', ':', ';', '"']
    manifest = make_manifest(text)
    stitch = rebuild(manifest)
    identical = (text == stitch)
    print(manifest)
    print(identical)
