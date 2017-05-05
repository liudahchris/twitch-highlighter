from chatty_reader import process_file
import time
import nvd3
from werkzeug.utils import secure_filename


def _make_clean_label(tokens):
    '''
    takes a list of words and formats them into nice label
    '''
    s = "Top Words: <br>\n"
    s += "<br> \n".join(tokens)
    return s


def nvd3_time(dt):
    '''
    Takes datetime object and returns a value for
    nvd3 plotting
    '''
    return time.mktime(dt.timetuple()) * 1000


def format_data(fname):
    '''
    '''
    data = process_file(fname)
    times, counts, labels = [], [], []
    for t in sorted(data):
        times.append(nvd3_time(t))
        counts.append(data[t]['counts'])
        labels.append(_make_clean_label(data[t]['words']))
    return times, counts, labels


def make_plot(fname):
    '''
    generates html plot
    '''
    x, y, labels = format_data(fname)
    name = secure_filename(fname)

    chart = nvd3.lineWithFocusChart(
        name=name,
        height='550',
        width='850',
        x_is_date=True,
        x_axis_format="%H:%M",
        focus_enable=True
    )

    chart.set_containerheader(name)

    labels = list(labels)

    chart.add_serie(
        x=x,
        y=y,
        # extra=extra
        text=labels
    )

    chart.buildhtml()

    with open('temp/temp.html', 'w') as f:
        f.write(chart.htmlcontent)

    return None
