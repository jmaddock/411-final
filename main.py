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
    params = {'endpoint':'music',
              'entitytype':'artist',}
    include = 'Moods,MusicBio,MusicStyles,Themes'
    includeList = ['moods','musicBio','musicStyles','themes']
    result = {}
    json = jsonIn['searchResponse']['results'][0]['name']
    result['name'] = json['name']
    result['children'] = []
    for  x in nodeList:
        result['children'].append({'name':x, 'children':[]})
    for x in result['children']:
        if json[x['name']]:
            count = 0
            for y in json[(x['name'])]:
                if x['name'] == 'aliases': #TODO: start here, start including data
                    result['Aliases'] = y
                else:
                    params['query'] = y['name']
                    z = getData(params = params, include = include)['searchResponse']['results'][0]['name']
                    if 'weight' in y:
                        x['children'].append({'name':y['name'],
                                              'Weight':y['weight'],
                                              'children':[]})
                        for a in includeList:
                            try:
                                x['children'][count][formatTitle(a)] = z[a][0]['name']
                            except:
                                print 'working...'
#                                              'moods':z['moods'][0],
#                                              'musicGeneres':z['musicGenres'][0],
#                                              'musicStyles':z['musicStyles'][0],
#                                              'themes':z['themes'][0],})
                    else:
                        x['children'].append({'name':y['name']})
                    count += 1
    for x in result['children']:
        x['name'] = formatTitle(x['name'])
    print pretty(result)
    return simplejson.dumps(result)

def expandTree(jsonIn, artist):
    jsonIn
    
def formatTitle(input):
    if input == 'aliases':
        return "Aliases"
    elif input == 'associatedWith':
        return "Associated Artists"
    elif input == 'collaboratorWith':
        return "Callaborated With"
    elif input == 'contemporaries':
        return "Contemporaries"
    elif input == "followers":
        return "Followers"
    elif input == 'groupMembers':
        return "Group Members"
    elif input == 'influencers':
        return "Influencers"
    elif input == 'memberOf':
        return "Member Of"
    elif input == 'similars':
        return "Similar Artists"
    elif input == 'moods':
        return "Mood"
    elif input == 'musicBio':
        return "Music Bio"
    elif input == 'musicStyles':
        return "Style"
    elif input == 'themes':
        return "Theme"
    else:
        return input
    

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
    
