import urllib.parse, urllib.request, urllib.error, json

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

def safeGet(url):
    try:
        return urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        if hasattr(e,"code"):
            print("The server couldn't fulfill the request.")
            print("Error code: ",e.code)
        elif hasattr(e,"reason"):
            print("We failed to reach a server")
            print("Error reason",e.reason)
        return None

import api_key

movieDB_api_key = api_key.movieDB_api

### get a list of genre from the database, and return a dictionary of 'genre:ID'
def getGenreList():
    baseurl = "https://api.themoviedb.org/3/genre/movie/list"
    param = {}
    param["api_key"] = movieDB_api_key
    url = baseurl + "?" + urllib.parse.urlencode(param)
    result = safeGet(url)
    if result is not None:
        genreData = json.load(result)
        genreDict = {}
        for genre in genreData["genres"]:
            genreDict[genre["name"].lower()] = genre["id"]
        return genreDict

### send in the ID and return a list of top 5 rated movie title
def getMovie(genreID):
    baseurl = "https://api.themoviedb.org/3/discover/movie"
    param = {}
    param["api_key"] = movieDB_api_key
    param["sort_by"] = "popularity.desc"
    param["page"] = "1"
    param["with_genres"] = genreID
    url = baseurl + "?" + urllib.parse.urlencode(param)
    result = safeGet(url)
    if result is not None:
        movieData = json.load(result)
        sortedList = sorted(movieData["results"], key=lambda x:x["vote_average"], reverse=True)[0:5]
        titleList = []
        for movie in sortedList:
            titleList.append(movie["title"])
        return titleList

### convert the user input (genre name) into computer recognizable ID, and call getMovie function
def converter(genre):
    # deal with error?, if genre not in list?
    genreID = getGenreList()[genre]
    return getMovie(genreID=genreID)

### Simulation of user input
print(converter(genre="romance"))