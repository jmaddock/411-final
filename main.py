import urllib, urllib2, time, hashlib
import json as simplejson

API_KEY = "xdc8ttebmyukvrzsxtby8hqc"
API_SECRET = "zgQj9ZTbwa"

# Pre : input a dictionary with the required params (artist name + filters required)
# Post: outputs a JSON formatted dictionary w/ requested data
# this method will probably be called multiple times for each viz in order to get info
# about both the "root" artist and the "leaf" artists
def getData(base = 'http://api.rovicorp.com/search/v2.1/music/search?',
            key = API_KEY,
            secret = API_SECRET,
            return_format = 'json',
            country = 'us',
            include = '',
            params = {}):
    
    params['apikey'] = key
    params['format'] = return_format
    params['country'] = country
    params['sig'] = sig()
    url = base + urllib.urlencode(params) + "&include="+include   
    try: 
        json = (convert(safeGet(url)))
        return json
    except:
        return None
# Pre : input JSON files in a dictionary, possibly multiple
# Post: returns JSON file formatted for the d3 basic network
def treeFormat(jsonIn, nodeList = []):
    result = {}
    json = jsonIn['searchResponse']['results'][0]['name']
    print pretty(json)
    result['name'] = json['aliases'][0]
    result['children'] = []
    for  x in nodeList:
        result['children'].append({'name':x, 'children':[]})
    print pretty(result)
    for x in result['children']:
        if json[x['name']]:
            print json[(x['name'])]
            for y in json[(x['name'])]:
                if x['name'] == 'aliases':
                    x['children'].append({'name':y})
                else:
                    x['children'].append({'name':y['name']})
    return result

# same method as above, but formats to encode geo-data
#TODO: def mapFormat():
    
def convert(restful):
    jsonresult = restful.read()
    return simplejson.loads(jsonresult)

def pretty(obj):
    return simplejson.dumps(obj, sort_keys=True, indent=2)
    
def safeGet(url):
    try:
        return urllib2.urlopen(url)
    except urllib2.URLError, e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
        return None

def sig():
        timestamp = int(time.time())
        m = hashlib.md5()
        m.update(API_KEY)
        m.update(API_SECRET)
        m.update(str(timestamp))
        return m.hexdigest()
