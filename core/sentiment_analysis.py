# tutorial from: https://programminghistorian.org/en/lessons/sentiment-analysis
# chart info: https://github.com/agiliq/django-graphos
import nltk
nltk.download('vader_lexicon')
nltk.download('punkt')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime
import numpy as np

# from core.models import Entries
# allEntries = Entries.objects.all()
# should pass an array of charts into the template and render accordingly

# to table fo all graphs
#

'''
Data is grouped by:
- Day of week x
- Time of day x
- Month of year x

Analysis for:
1. pos/neg
'''

# next, we initialize VADER so we can use it within our Python script
sid = SentimentIntensityAnalyzer()
# the variable 'message_text' now contains the text we will analyze.
# input texts needs ''' quotes before and after
message_text = '''Like you, I am getting very frustrated with this process. I am genuinely trying to be as reasonable as possible. I am not trying to "hold up" the deal at the last minute. I'm afraid that I am being asked to take a fairly large leap of faith after this company (I don't mean the two of you -- I mean Enron) has screwed me and the people who work for me.'''

# Calling the polarity_scores method on sid and passing in the message_text outputs a dictionary with negative, neutral, positive, and compound scores for the input text
scores = sid.polarity_scores(message_text)

# Here we loop through the keys contained in scores (pos, neu, neg, and compound scores) and print the key-value pairs on the screen
# for key in sorted(scores):
   # print('{0}: {1}, '.format(key, scores[key]), end='')

# scores prints: compound: -0.3804, neg: 0.093, neu: 0.836, pos: 0.071,

#  Researchers may wish to set a minimum threshold for positivity or negativity
#  before they declare a text definitively positive or negative – for instance,
#  the official VADER documentation suggests a threshold of -0.5 and 0.5
def split_by_season(entries):
    month_avg = get_by_month(entries)
    spring = []
    winter = []
    fall = []
    summer = []
    for i in range(len(month_avg)):
        if i < 3 or i > 10:
            for month in month_avg[i]:
                winter.append(month)
        elif i > 2 and i < 6:
            for month in month_avg[i]:
                spring.append(month)
        elif i > 5 and i < 9:
            for month in month_avg[i]:
                summer.append(month)
        elif i > 8 and i < 11:
            for month in month_avg[i]:
                fall.append(month)
    spring_pie = compute_scores_pie(spring)
    fall_pie = compute_scores_pie(fall)
    winter_pie = compute_scores_pie(winter)
    summer_pie = compute_scores_pie(summer)
    current_month_pie = compute_scores_pie(get_this_month(entries))
    return [spring_pie, fall_pie, winter_pie, summer_pie, current_month_pie]


def split_by_day(entries):
    week_avg = get_by_day_week(entries)
    weekday = []
    weekend = []
    for i in range(len(week_avg)):
        if i > 0 and i < 6:
            for day in week_avg[i]:
                weekday.append(day)
        else:
            for day in week_avg[i]:
                weekend.append(day)
    weekday_pie = compute_scores_pie(weekday)
    weekend_pie = compute_scores_pie(weekend)
    return [weekday_pie, weekend_pie]


def split_by_time(entries):
    time_avg = get_by_time_of_day(entries)
    morning_pie = compute_scores_pie(time_avg[0])
    afternoon_pie = compute_scores_pie(time_avg[1])
    evening_pie = compute_scores_pie(time_avg[2])
    night_pie = compute_scores_pie(time_avg[3])
    return [morning_pie, afternoon_pie, evening_pie, night_pie]


def create_avgs(entries):
    total_avg = compute_scores_avg(entries)
    current_month_avg = compute_scores_avg(get_this_month(entries))
    return [total_avg, current_month_avg]


def compute_scores_pie(entries):
    # compound: -0.3804, neg: 0.093, neu: 0.836, pos: 0.071
    # entries = entries.order_by('-created_at')
    neg = 0
    neu = 0
    pos = 0
    for entry in entries:
        scores = SentimentIntensityAnalyzer().polarity_scores(entry.text)
        neg += scores["neg"]
        neu += scores["neu"]
        pos += scores["pos"]
    if len(entries) > 0:
        len_entries = len(entries)
        sentiment_vect = [neg/len(entries), neu/len(entries), pos/len(entries)]
        return sentiment_vect
    else:
        return [0, 0, 0]

# for list of Entry object, outputs vector of sentiment analysis
def compute_scores_vector(entries):
    # entries = entries.order_by('-created_at')
    sentiment_vect = []
    for entry in entries:
        scores = SentimentIntensityAnalyzer().polarity_scores(entry.text)
        sentiment_vect.append(scores["compound"])
    return sentiment_vect

# for list of Entry objects, outputs avg entry score
def compute_scores_avg(entries):
    sentiment_vect = 0
    for entry in entries:
        scores = SentimentIntensityAnalyzer().polarity_scores(entry.text)
        sentiment_vect += (scores["compound"])
    if len(entries) > 0:
        return sentiment_vect/len(entries)
    else:
        return 0


# outputs list of list of entries by time of day
def get_by_time_of_day(all_entries):
    morning_entries = []
    afternoon_entries = []
    evening_entries = []
    night_entries = []
    for entry in all_entries:
        if float(entry.created_at.strftime("%H")) < 12:
            morning_entries.append(entry)
        elif float(entry.created_at.strftime("%H")) < 17:
            afternoon_entries.append(entry)
        elif float(entry.created_at.strftime("%H")) < 20:
            evening_entries.append(entry)
        else:
            night_entries.append(entry)
    entry_array = [morning_entries, afternoon_entries, evening_entries, night_entries]
    return entry_array

# outputs list of list of entries by day of week
def get_by_day_week(all_entries):
    mon = []
    tues = []
    weds = []
    thurs = []
    fri = []
    sat = []
    sun = []
    for entry in all_entries:
        if float(entry.created_at.strftime("%w")) == 1:
            mon.append(entry)
        elif float(entry.created_at.strftime("%w")) == 2:
            tues.append(entry)
        elif float(entry.created_at.strftime("%w")) == 3:
            weds.append(entry)
        elif float(entry.created_at.strftime("%w")) == 4:
            thurs.append(entry)
        elif float(entry.created_at.strftime("%w")) == 5:
            fri.append(entry)
        elif float(entry.created_at.strftime("%w")) == 6:
            sat.append(entry)
        elif float(entry.created_at.strftime("%w")) == 0:
            sun.append(entry)
    entry_array = [mon, tues, weds, thurs, fri, sat, sun]
    return entry_array

# outputs list of list of entries by month
def get_by_month(all_entries):
    jan = []
    feb = []
    mar = []
    apr = []
    may = []
    jun = []
    jul = []
    aug = []
    sep = []
    oct = []
    nov = []
    dec = []
    for entry in all_entries:
        if float(entry.created_at.strftime("%m")) == 1:
            jan.append(entry)
        elif float(entry.created_at.strftime("%m")) == 2:
            feb.append(entry)
        elif float(entry.created_at.strftime("%m")) == 3:
            mar.append(entry)
        elif float(entry.created_at.strftime("%m")) == 4:
            apr.append(entry)
        elif float(entry.created_at.strftime("%m")) == 5:
            may.append(entry)
        elif float(entry.created_at.strftime("%m")) == 6:
            jun.append(entry)
        elif float(entry.created_at.strftime("%m")) == 7:
            jul.append(entry)
        elif float(entry.created_at.strftime("%m")) == 8:
            aug.append(entry)
        elif float(entry.created_at.strftime("%m")) == 9:
            sep.append(entry)
        elif float(entry.created_at.strftime("%m")) == 10:
            oct.append(entry)
        elif float(entry.created_at.strftime("%m")) == 11:
            nov.append(entry)
        elif float(entry.created_at.strftime("%m")) == 12:
            dec.append(entry)
    entry_array = [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]
    return entry_array

def get_this_month(all_entries):
    now = datetime.now()
    now_year = now.strftime("%Y")
    now_month = now.strftime("%m")
    this_month = []
    for entry in all_entries:
        if float(entry.created_at.strftime("%m")) == now_month and entry.created_at.strftime("%Y") == now_year:
            this_month.append(entry)
    return this_month


# outputs vector of average sentiments for an array of arrays of entry sorted by some predetermined category
def compute_by_aggregation(entry_array):
    sentiment_vect = []
    for entry in entry_array:
        sentiment_vect.append(compute_scores_avg(entry))
    return sentiment_vect


def create_by_time(entries):
    y_axis = compute_by_aggregation(get_by_time_of_day(entries))
    x_axis = ["morning", "afternoon", "evening", "night"]
    return x_axis, y_axis


def create_by_day(entries):
    y_axis = compute_by_aggregation(get_by_day_week(entries))
    x_axis = ["mon", "tues", "weds", "thurs", "fri", "sat", "sun"]
    return x_axis, y_axis


def create_by_month(entries):
    y_axis = compute_by_aggregation(get_by_month(entries))
    x_axis = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    return x_axis, y_axis

def create_this_month(entries):
    y_axis = compute_by_aggregation(get_this_month(entries))
    x_axis = np.linspace([1, 30, 30])
    return x_axis, y_axis



def create_all(entries):
    y_axis = compute_scores_vector(entries)
    x_axis = []
    x_ticks = []
    for entry in entries:
        year = float(entry.created_at.strftime("%Y")) - 2020
        month = float(entry.created_at.strftime("%m"))
        day = float(entry.created_at.strftime("%w"))
        hour = float(entry.created_at.strftime("%H"))
        day_str = entry.created_at.strftime("%d")
        month_str = entry.created_at.strftime("%b")
        tick_name = month_str + " " + day_str
        time_in_hours = year*24*365 + 30*24*month + 24*day + hour
        x_axis.append(time_in_hours)
        x_ticks.append(tick_name)
    return x_axis, y_axis, x_ticks






