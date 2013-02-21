import main

include = 'Aliases,AssociatedWith,CollaboratorWith,Contemporaries,Followers,GroupMembers,Influencers,MemberOf,Similars'
query = 'eric clapton'
params = {'endpoint':'music',
          'entitytype':'artist',
          'query':query,}
main.getData(params = params, include = include)
