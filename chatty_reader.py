from collections import Counter, defaultdict


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
    pass


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
    pass


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


def parse_message(line):
    '''
    Gets the information of a single line from Chatty chat log

    Parameters:
    line: string
        line of text from chat log

    Returns:
    time : Time of message
    '''
    pass


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


def process_file(fname, n_words=10):
    '''
    '''
    # Dictionary timestamp as key and word count dictionary as value
    data = defaultdict(dict)
    with open(fname) as f:
        for i, line in enumerate(f):
            if is_message(line):
                time, word_counts = parse_message(line)
                data[time]['words'] = merge_counters([data.get(time, Counter()), word_counts])
                data[time]['counts'] = data[time].get('counts', 0) + 1

                # Some stuff to reduce space
                if i == 0:
                    previous_time = time
                if time != previous_time:
                    data[previous_time]['words'] = [word for word, _ in
                                                    data[previous_time]['words'].most_common(n_words)]
                    previous_time = time

                # Write empty points if no messages in certain time
    return data
