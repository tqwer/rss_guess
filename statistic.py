#statistic posting's public time

import urllib
from xml.dom import minidom
import datetime
from email.utils import parsedate

# get public time of entry in rss feed
def get_public_times(rss_url):
    xmldom = minidom.parse(urllib.urlopen(rss_url))
    publics = xmldom.getElementsByTagName('pubDate') # rss version 2.0
    if len(publics) == 0:
        publics = xmldom.getElementsByTagName('published')  # rss version 1.0
    result = []
    for e in publics:
        result.append(parsedate(e.childNodes[0].nodeValue))
    return result
# times is result of get_public_times
# time[i] like (2012, 4, 20, 7, 31, 28, 0, 1, -1)
def stat_by_year(times):
    dic = {}
    for time in times:
        if time[0] in dic:
            dic[time[0]] += 1
        else:
            dic[time[0]] = 1
    return dic

# times is result of get_public_times
# time[i] like (2012, 4, 20, 7, 31, 28, 0, 1, -1)
def stat_by_month(times):
    num_year = len(stat_by_year(times))
    dic = {}
    for time in times:
        if time[1] in dic:
            dic[time[1]] += 1.0/num_year
        else:
            dic[time[1]] = 1.0/num_year
    return dic

# times is result of get_public_times
# time[i] like (2012, 4, 20, 7, 31, 28, 0, 1, -1)
def stat_by_weekday(times):
    num_week = len(stat_by_year(times)) * 52
    dic = {}
    for time in times:
        weekday = datetime.date(time[0], time[1], time[2]).weekday();       # 0 is monday, 6 is Sunday
        if weekday in dic:
            dic[weekday] += 1.0/num_week
        else:
            dic[weekday] = 1.0/num_week
    return dic

# times is result of get_public_times
# time[i] like (2012, 4, 20, 7, 31, 28, 0, 1, -1)
def stat_by_hour(times):
    num_day = len(stat_by_year(times)) * 365
    dic = {}
    for time in times:
        if time[3] in dic:
            dic[time[3]] += 1.0/num_day
        else:
            dic[time[3]] = 1.0/num_day
    return dic

times = get_public_times('http://www.udacity-forums.com/cs101/questions/?type=rss')

print stat_by_year(times)
print stat_by_month(times)
print stat_by_weekday(times)
print stat_by_hour(times)