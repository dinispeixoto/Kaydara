import re

# extract all words in a string
def gen_array(links):
    splitted = links.split(",")
    res = []
    for l in splitted:
        res.append(l.strip())
    return res 


# remove quotes in a message
def rm_quotes(msg):
    return msg.replace('"','')


# remove the string "subject"
def rm_subject(msg):
    return re.sub(r"[Ss]ubject: *", '', msg)