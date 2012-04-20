from rss_guess2 import *

u = split('http://www.udacity-forums.com/cs101/questions/52159/contest-announcement-and-submissions?sort=votes&page=6?')
r = split('http://www.udacity-forums.com/cs101/questions/52159/contest-announcement-and-submissions?type=rss')
print '\n', u, '\n', r
rule = find_rule(u, r)
print rule
u = split('http://www.udacity-forums.com/cs101/questions/52159/contest-announcement-and-submissions')
print rss_guess(rule, u)


u = split('http://www.bbc.co.uk/news/')
r = split('http://feeds.bbci.co.uk/news/rss.xml')
print '\n', u, '\n', r
rule = find_rule(u, r)
print rule
u = split('http://www.bbc.co.uk/news/uk/')
print rss_guess(rule, u)


# feature:
# change order of word:
# news/wolds  -> would/news
u = split('http://www.bbc.co.uk/news/would')
r = split('http://feeds.bbci.co.uk/would/news/rss.xml')
print '\n', u, '\n', r
rule = find_rule(u, r)
print rule
u = split('http://www.bbc.co.uk/news/would/uk')
print rss_guess(rule, u)