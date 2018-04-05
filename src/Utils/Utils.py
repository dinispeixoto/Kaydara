# extract all words in a string
def gen_array(links):
    splitted = links.split("\n ")
    res = []
    for l in splitted:
        res.append(l.strip())
    return res