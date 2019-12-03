import urllib.parse, urllib.request, urllib.error, json

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

# handle any errors due to HTTP or connection related exceptions
def safeGet(url):
    try:
        return urllib.request.urlopen(url)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print("The server couldn't fulfill the request.")
            print("Error code: ", e.code)
        elif hasattr(e,'reason'):
            print("We failed to reach a server")
            print("Reason: ", e.reason)
        return None

import api_key

omdb_api_key = api_key.omdb_api

# return a dictionary with movie info data from the API call
movie_title = 'The Lion King'
def getMovieInfo(t=movie_title):
    base_url = 'http://www.omdbapi.com/'
    api_key = omdb_api_key
    api_key_str = '?apikey=' + api_key
    params = {}
    params['t'] = t  # movie title to search for
    paramstr = urllib.parse.urlencode(params)
    omdbrequest = base_url + api_key_str + '&' + paramstr
    result = safeGet(omdbrequest)
    if result is not None:
        movieinfo_data = json.load(result)
        return movieinfo_data
    else:
        return "Sorry, couldn't retrieve the movie information."


print(pretty(getMovieInfo()))  # printing out the dictionary

def basic_movieinfo(t=movie_title):
    movieinfo = getMovieInfo(t=t)
    print('About "%s"'%t)
    print('Released Year: %s' % movieinfo['Year'])
    print('Genre: %s' % movieinfo['Genre'])
    print('Rated: %s' % movieinfo['Rated'])
    print('The plot: %s' % movieinfo['Plot'])
    print("imdbRating: %s" % movieinfo['imdbRating'])
    print("imdbVotes: %s" % movieinfo['imdbVotes'])


def get_rating(t=movie_title, rating_source='Internet Movie Database'):
    movieinfo = getMovieInfo(t=t)
    ratings = movieinfo['Ratings']
    for rating in ratings:
        if rating['Source'] == rating_source:
            print('The rating is %s for %s based on %s' % (rating['Value'], t, rating_source))

print("------------------------")
basic_movieinfo()

print("------------------------")
# ratings for multiple movies
print("These are the ratings for multiple movies:\n")
movies = ['The Lion King', 'The Little Mermaid', 'The Incredibles', 'Aladdin', 'Frozen', 'Finding Dory', 'Mulan']
for movie in movies:
    get_rating(t=movie)

print("------------------------")
# ratings from different sources for one movie
print("These are the ratings for one movie:\n")
rating_sources = ['Internet Movie Database', 'Rotten Tomatoes', 'Metacritic']
for rating_source in rating_sources:
    get_rating(rating_source=rating_source)
