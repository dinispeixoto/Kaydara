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


# parse date
def parse_date(date):
    if re.match(r"(\d{4})-(\d{2})-(\d{2})T(.+)\+", date) is not None:
        match = re.findall(r"(\d{4})-(\d{2})-(\d{2})T(.+)\+", date)
        return match[0][2] + '/' + match[0][1] + '/' + match[0][0] + ' at ' + match[0][3]
    else:
        match = re.findall(r"(\d{4})-(\d{2})-(\d{2})", date)
        return match[0][2] + '/' + match[0][1] + '/' + match[0][0]


# convert date to a universal format
def encode_msg(msg):
    return re.sub(r"\n", ' .. ', msg)

def decode_msg(msg):
    return re.sub(r" \.\. ", '\n', msg)