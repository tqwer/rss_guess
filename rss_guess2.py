import re

# split url into array
def split(s):
    return re.findall('[/&?.=]+|[^/&?.=]+', s)


def find_common(u, r):
    rs = []
    for e in u:
        if e in r:
            del(r[r.index(e)])
        else:
            rs.append(e)
    return rs, r
# define is_array function
is_array = lambda var: isinstance(var, (list))

# a sorted in increasing order, a is list of number
# e is number need to find
# return [i, di, j, dj]
# 0<= j - i <= 1
# a[i] + di = e
# e + 1 = a[j] + dj

def find_bound(a, e):
    for i in range(0, len(a)):
        if a[i] > e:
            if e + 1 == a[i]:
                return [i-1, e - a[i-1], i, 0]
            else:
                return [i-1, e - a[i-1], i-1, e - a[i-1] + 1]
    return None

# find all element in list u and doesn't appear in list r
# if one element appear n times in u, it have to appear n times in r
# return: list of order of above elements
# first order of list is 1
def find_in_list(u, r):
    rs, nu, nr = [], list(u), list(r)
    for i in range(0, len(nu)):
        if nu[i] in nr:
            del(nr[nr.index(nu[i])])
        else:
            rs.append(i+1)
    return rs
# take a webpage url (u), and it's associated rss feed url (r).
# return a rule to guess rss_url
def find_rule(u, r):
    print u, r
    ru = find_in_list(u, r)
    ru.insert(0, 0)
    ru.append(len(u) + 1)
    rr = []
    for e in r:
        if e in u:
            i = u.index(e) + 1
            u[i-1] = []
            bound = find_bound(ru, i)
            if len(rr) > 0 and is_array(rr[-1]) and rr[-1][2] == bound[0] and rr[-1][3] == bound[1]:
                rr[-1][2] = bound[2]
                rr[-1][3] = bound[3]
            else:
                rr.append(bound)
        else:
            rr.append(e)

    return [u[i-1] for i in ru[1:-1]], rr

# rule is result of  find_rule
# u is a list associate with url of webpage, that need to find rss feed link
# u is result of split
def rss_guess(rule, u):
    rr = [0]
    for e in rule[0]:
        try:
            rr.append(u.index(e, rr[-1])+1)
        except:
            rr.append(-1)
    rr.append(len(u)+1)
    # find result rss string
    rss = ''
    for e in rule[1]:
        if is_array(e):
            if rr[e[0]] == -1 or rr[e[2]] == -1:
                return ''
            rss += ''.join(u[rr[e[0]]+e[1]-1 : rr[e[2]]+e[3]-1])
        else:
            rss += e
    return rss


