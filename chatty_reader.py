from collections import Counter, defaultdict
import string
from nltk.corpus import stopwords
import datetime


def is_start(line):
    '''
    Checks if line signals start or end of session
    These lines begin with #

    Parameters:
    line : string
        line of text from chat log

    Returns:
    is_start_end : bool
        if line is start of end of session
    '''
    return line[:15] == "# Log started: "


def is_end(line):
    '''
    Checks if line signals start or end of session
    These lines begin with #

    Parameters:
    line : string
        line of text from chat log

    Returns:
    is_start_end : bool
        if line is start of end of session
    '''
    return line[:14] == "# Log closed: "


def is_message(line):
    '''
    Checks if a line is a chat message or not.
    The line is deemed a message if the second
    element is a username enclosed by "<>".

    Parameters:
    line: string
        line of text from chat log

    Returns:
    is_message: bool
        Whether the line is a chat message
    '''
    if len(line.split()) > 2:
        username = line.split()[1]
        return username[0] == '<' and username[-1] == '>'
    return False


def clean_token(token):
    '''
    Takes a token, strips punctuation and makes lowercase

    Parameters:
    token : string

    Returns:
    clean_ token : string
    '''
    return token.lower().translate(None, string.punctuation)


def clean_tokens(tokens):
    '''
    Takes a list of tokens and strips punctuation and makes all lowercase

    Parameters:
    tokens : list
        list of words

    Returns:
    clean_tokens : list
        list of lowercase words without punctuation
    '''
    tokens = clean_token(' '.join(tokens)).split()
    return [token for token in tokens
            if token not in stopwords.words('english')]


def parse_message(line):
    '''
    Gets the information of a single line from Chatty chat log

    Parameters:
    line: string
        line of text from chat log

    Returns:
    time : datetime
        Time of message
    word_counts: dictionary
        word counts of message
    '''
    TIME_FORMAT = "[%H:%M:%S]"
    tokens = line.split()
    time = datetime.datetime.strptime(tokens.pop(0), TIME_FORMAT).time()
    username = tokens.pop(0)
    # After popping off time, the username is at the head of the list
    word_counts = Counter(clean_tokens(tokens))
    return time, username, word_counts


def merge_counters(counters):
    '''
    Takes a list of counters and merges them into one.

    Parameters:
    counters : list of dictionaries
        dictionaries to track counts

    Returns:
    merged: dictionary
        merged counter dictionary
    '''
    if len(counters) < 1:
        return Counter()
    if len(counters) == 1:
        return counters.pop()
    merged = counters.pop()
    for c in counters:
        for key in c:
            merged[key] = c[key] + merged.get(key, 0)
    return merged


def get_top_words(word_counts, n_words):
    '''
    Gets the top n words from a word_count dictionary

    Parameters:
    word_counts : Counter (dict)
    n_words : int

    Returns :
    top_words : list of length n_words
    '''
    top_words = [word for word, _ in word_counts.most_common(n_words)]
    return top_words


def round_minute(dt):
    '''
    Rounds the a datetime object down to last minute

    Parameters:
    dt : datetime object

    Returns:
    rounded_dt : datetime object
    '''
    return dt - datetime.timedelta(seconds=dt.second)


def fill_blanks(time, previous_time, data):
    '''
    '''
    while time - previous_time > datetime.timedelta(minutes=1):
        previous_time += datetime.timedelta(minutes=1)
        data[previous_time] = {'counts': 0, 'words': []}
    return data


def process_file(fname, n_words=10):
    '''
    Takes a text file and processes it. Bins messages into

    Parameters:
    fname : string
        location of chatty text file

    n_words : int (default 10)
        number of top words to keep
    '''
    # Dictionary timestamp as key and word count dictionary as value
    DATE_FORMAT = "%Y-%m-%d"
    data = defaultdict(dict)
    previous_time = None
    with open(fname) as f:
        for i, line in enumerate(f):
            if is_start(line):
                start_dt = line[15:]
                start_date, start_time, _ = start_dt.split()
                date = datetime.datetime.strptime(start_date, DATE_FORMAT)

            if is_end(line):
                end_dt = line[14:]
                end_date, end_time, _ = end_dt.split()
                break

            elif is_message(line):
                time, username, word_counts = parse_message(line)
                time = round_minute(datetime.datetime.combine(date, time))

                if not previous_time:
                    previous_time = time

                # Midnight edge case
                if time < previous_time:
                    date += datetime.timedelta(days=1)

                data[time]['words'] = merge_counters([data.get(time, dict()).get('words', Counter()), word_counts])
                data[time]['counts'] = data[time].get('counts', 0) + 1

                # Some stuff to reduce space
                if time != previous_time:
                    data[previous_time]['words'] = get_top_words(data[previous_time].get('words', Counter()), n_words)
                    # Write empty points if no messages in certain time
                    data = fill_blanks(time, previous_time, data)
                    previous_time = time

    # Outside of loop, get the top words of the last time
    data[time]['words'] = get_top_words(data[time]['words'], n_words)
    return data
