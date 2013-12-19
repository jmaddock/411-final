import data

#this should probably be 'all' in the final
def run():
    include = 'Aliases,AssociatedWith,CollaboratorWith,Contemporaries,Followers,GroupMembers,Influencers,MemberOf,Similars,Images,Moods,MusicBio,MusicStyles,Themes,Web'
    nodeList = ['associatedWith', 'collaboratorWith', 'contemporaries', 'followers', 'groupMembers', 'influencers', 'similars']
    query = 'eric clapton'
    params = {'endpoint':'music',
              'entitytype':'artist',
              'query':query,}
    json = data.getData(params = params, include = include)
    print json
    #return data.treeFormat(json, nodeList)

def main():
    run()

if __name__ == "__main__":
    main()
