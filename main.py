import os, urllib, jinja2, webapp2, data

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def post(self):
        include = 'Aliases,AssociatedWith,CollaboratorWith,Contemporaries,Followers,GroupMembers,Influencers,MemberOf,Similars,Images,Moods,MusicBio,MusicStyles,Themes,Web'
        nodeList = ['associatedWith', 'collaboratorWith', 'contemporaries', 'followers', 'groupMembers', 'influencers', 'similars']
        query = self.request.get('query')
        params = {'endpoint':'music',
                  'entitytype':'artist',
                  'query':query}
        json = data.getData(params = params, include = include)
        json = data.treeFormat(json, nodeList)
        template = JINJA_ENVIRONMENT.get_template('view.html')
        self.response.write(template.render({'data':json}))

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({}))

application = webapp2.WSGIApplication([
    ('/*', MainPage),
], debug=True)
