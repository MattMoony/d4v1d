import enum, os, json, time
from lib import params

class DataType(enum.Enum):
    FOLLOWERS = ('o', 'followers.json')
    FOLLOWING = ('i', 'following.json')

def store(uname, data, _type=DataType.FOLLOWERS):
    outd = os.path.abspath(os.path.join(params.TMP_PATH, '{}/{}{}'.format(uname, _type.value[0], str(time.time()))))
    if not os.path.isdir(outd):
        os.makedirs(outd)
    with open(os.path.join(outd, _type.value[1]), 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)

def store_followers(uname, data):
    store(uname, data, DataType.FOLLOWERS)

def store_following(uname, data):
    store(uname, data, DataType.FOLLOWING)

def load(uname, _type=DataType.FOLLOWERS):
    upath = os.path.abspath(os.path.join(params.TMP_PATH, uname))
    if not os.path.isdir(upath):
        return []
    opts = [d for d in os.listdir(upath) if os.path.isdir(os.path.join(upath, d)) and d.startswith(_type.value[0]) and os.path.isfile(os.path.join(upath, d, _type.value[1]))]
    if not opts:
        return []
    opts.sort()
    for i in range(len(opts))[::-1]:
        try:
            with open(os.path.join(upath, opts[i], _type.value[1])) as f:
                return json.load(f)
        except:
            pass
    return []

def load_followers(uname):
    return load(uname, DataType.FOLLOWERS)

def load_following(uname):
    return load(uname, DataType.FOLLOWING)