LOGIN: str = 'https://i.instagram.com/api/v1/accounts/login/'
FOLLOWERS: str = 'https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={}'
FOLLOWING: str = 'https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables={}'
MEDIA: str = 'https://www.instagram.com/graphql/query/?query_hash=e769aa130647d2354c40ea6a439bfc08&variables={}'
# --> IINFO will only give you all the user information, if you're signed in ... 
# otherwise, all you'll get is the uid, the uname and the profile pic URL ... 
IINFO: str = 'https://i.instagram.com/api/v1/users/{}/info/'
# --> UINFO works for anyone ... (won't provide everything about private users, obviously)
UINFO: str = 'https://www.instagram.com/{}/?__a=1'

# prefix n for "normie"
N_LOGIN: str = 'https://www.instagram.com/accounts/login'
N_PROFILE: str = 'https://www.instagram.com/{}'