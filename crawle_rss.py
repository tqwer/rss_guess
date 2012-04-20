import urllib
import HTMLParser
import re
import urlparse
from xml.dom import minidom
from rss_guess2 import *

#remove fragment in url
#ex: http://bbc.co.uk/#abc -> http://bbc.co.uk/
def remove_fragment(url):
    i = url.find('#')
    if i == -1:
        return trim_url(url)
    else:
        return trim_url(url[0:i])
# remove lastest character of string if it is '/','&','?','.','='
# and remove www in hosting name
# ex: http://www.bbc.co.uk/ -> http://bbc.co.uk
def trim_url(url):
    if url[-1] in ['/','&','?','.','=']:
        return trim_url(url[0:-1])
    return url.replace('://www.', '://', 1)

# get content of webpage associated with url
def get_content(url):
    conn = urllib.urlopen(url)
    output = unicode(conn.read(), 'utf8')
    conn.close()
    parser = HTMLParser.HTMLParser()
    content = parser.unescape(output)
    return content

# get all link from url's content
# all links in absolute
def get_links(url):
    content = get_content(url)
    urls = re.findall('<a.*?href="(.*?)"', content)
    for i in range(0, len(urls)):
        urls[i] = remove_fragment(urlparse.urljoin(url, urls[i], False))
    return urls

# check if a url is rss feed link
# this just check it's content-type is xml or not
# just simple
def is_rss_link(url):
    try:
        if url.startswith('http') == False:
            return False
        conn = urllib.urlopen(url)
        header = conn.info().dict
        if 'content-type' in header and header['content-type'] in ['text/xml', 'application/rss+xml']:
            return True
        return False
    except:
        return False

# get associate webpage with rss feed url
# this use <link> tag in channel
# this will not work for rss use dtd in xml file
# ex: <rss xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">
# <atom:link href="http://www.udacity-forums.com/cs101/questions/">
# just simple
def get_associate_site(rss_url):
    xmldoc = minidom.parse(urllib.urlopen(rss_url))
    if xmldoc:
        link = xmldoc.getElementsByTagName('link')[0]
        return remove_fragment(link.childNodes[0].nodeValue)
    return None
# take a rss url, and list of webpage urls as input
# and return list of [url, rss_url]
# rss_url associte with url
# this function will guess rss_link for each url in urls
# and check that rss_link by is_rss_link(..)
def rss_guess_engine(rss_url, urls):

    associate_url = get_associate_site(rss_url)
    if associate_url == None:
        return None
    rule = find_rule(split(associate_url), split(rss_url))
    print rule
    #guess
    result = [[associate_url, rss_url]]
    for url in urls:
        rss = rss_guess(rule, split(trim_url(url)))
        print 'guess: ' + url +  '         '+ rss
        if rss != None and is_rss_link(rss):
            result.append([url, rss])
    return result

# take list of seed pages as input
# them have to have same host
# and return list of [url, rss_url]
# ex: crawle_rss(['http://bbc.co.uk'])
# output:
# [['http://bbc.co.uk/sport/','http://www.bbc.co.uk/news/sport/rss.xml']
# ['http://bbc.co.uk/news', 'http://feeds.bbci.co.uk/news/rss.xml']
#.........................
#.........
#]

def crawle_rss(seed):
    to_crawle = seed
    crawled = []
    while to_crawle:
        url = to_crawle.pop()
        crawled.append(url)
        print 'crawling: ' + url
        if is_rss_link(url):
            return rss_guess_engine(url, to_crawle)
        urls = get_links(url)
        for e in urls:
            if e not in crawled and e not in to_crawle:
                if e.find('rss') != -1 or e.find('feed') != -1:
                    to_crawle.append(e)
                else:
                    to_crawle.insert(0, e)
    return []

print crawle_rss(['http://www.bbc.co.uk/'])
