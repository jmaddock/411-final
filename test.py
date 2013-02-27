import main

#this should probably be 'all' in the final
include = 'Aliases,AssociatedWith,CollaboratorWith,Contemporaries,Followers,GroupMembers,Influencers,MemberOf,Similars'
nodeList = ['aliases', 'associatedWith', 'collaboratorWith', 'contemporaries', 'followers', 'groupMembers', 'influencers', 'memberOf', 'similars']
query = 'eric clapton'
params = {'endpoint':'music',
          'entitytype':'artist',
          'query':query,}
json = main.getData(params = params, include = include)
main.treeFormat(json, nodeList)
