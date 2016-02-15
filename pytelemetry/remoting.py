def translate(topic):
    opts = None
    t = topic
    try:
        split = str.split(topic,":")

        if len(split) > 1:
            t = split[0]
            opts = dict()
            opts['index'] = int(split[1])
    except ValueError:
        t = topic
        opts = None

    return t, opts
