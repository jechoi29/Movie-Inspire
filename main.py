import webapp2, os, urllib2, urllib, json, jinja2, logging
import api_key

omdb_api_key = api_key.omdb_api
movieDB_api_key = api_key.movieDB_api

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                       extensions=['jinja2.ext.autoescape'],
                                       autoescape=True)
def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

# handle any errors due to HTTP or connection related exceptions
def safeGet(url):
    try:
        return urllib2.urlopen(url)
    except urllib2.HTTPError as e:
        if hasattr(e,"code"):
            logging.error("The server couldn't fulfill the request.")
            logging.error("Error code: ", e.code)
        elif hasattr(e,'reason'):
            logging.error("We failed to reach a server")
            logging.error("Reason: ", e.reason)
        return None

# return a dictionary with movie info data from the API call
movie_title = 'The Lion King'
def getMovieInfo(t=movie_title):
    base_url = 'http://www.omdbapi.com/'
    api_key = omdb_api_key
    api_key_str = '?apikey=' + api_key
    params = {}
    params['t'] = t  # movie title to search for
    paramstr = urllib.urlencode(params)
    omdbrequest = base_url + api_key_str + '&' + paramstr
    result = safeGet(omdbrequest)
    if result is not None:
        movieinfo_data = json.load(result)

        return movieinfo_data
    else:
        return "Sorry, couldn't retrieve the movie information."


print(pretty(getMovieInfo()))  # printing out the dictionary

class Movie():
    def __init__(self, movie_dict):
        self.title = movie_dict['Title']
        self.year = movie_dict['Year']
        self.rated = movie_dict['Rated']
        self.released = movie_dict['Released']
        self.runtime = movie_dict['Director']
        self.writer = movie_dict['Writer']
        self.actors = movie_dict['Actors']
        self.plot = movie_dict['Plot']
        self.poster = movie_dict['Poster']
        self.metascore = movie_dict['Metascore']
        self.imdb_rating = movie_dict['imdbRating']
        self.imdb_votes = movie_dict['imdbVotes']
        self.imdbID = movie_dict['imdbID']
        # self.box_office = movie_dict['BoxOffice']
        # self.website = movie_dict['Website']


### Movie Database
def getMovie(genre_id):
    baseurl = "http://api.themoviedb.org/3/discover/movie"
    param = {}
    param["api_key"] = movieDB_api_key
    param["sort_by"] = "popularity.desc"
    param["page"] = "1"
    param["with_genres"] = genre_id
    url = baseurl + "?" + urllib.urlencode(param)
    result = safeGet(url)
    if result is not None:
        movieData = json.load(result)
        sortedList = movieData["results"][0:5]
        # sortedList = sorted(movieData["results"], key=lambda x:x["vote_average"], reverse=True)[0:5]
        titleList = []
        for movie in sortedList:
            titleList.append(movie["title"])
        return titleList

# class LandingHandler(webapp2.RequestHandler):
#     def get(self):
#         vals = {}
#         template = JINJA_ENVIRONMENT.get_template('landingpage.html')
#         self.response.write(template.render(vals))
#
#
#
# class MainHandler(webapp2.RequestHandler):
#     def get(self):p
#         genre_id = self.request.get('genre')
#         vals = {}
#         #movies = [Movie(getMovieInfo(t="The Lion King")), Movie(getMovieInfo(t="Frozen"))]
#         movies = [Movie(getMovieInfo(t=movie_title)) for movie_title in getMovie(genre_id=genre_id)]
#         vals["movies"] = movies
#         template = JINJA_ENVIRONMENT.get_template('outputpage.html')
#         self.response.write(template.render(vals))
#
#         # vals = {}
#         # vals["movies"] = [Movie(getMovieInfo(t="The Lion King")), Movie(getMovieInfo(t="Frozen"))]
#         # template = JINJA_ENVIRONMENT.get_template('landingpage.html')
#         # self.response.write(template.render(vals))
#
#
#         # go = self.request.get("submitButton")
#         # if genreID:
#         #
#         #     templateValues = {"message":"Top 5 Pugs Pictures by Views"}
#         #
#         #
#         #     template = JINJA_ENVIRONMENT.get_template('template.html')
#         #     self.response.write(template.render(templateValues))

# class MainHandler(webapp2.RequestHandler):
#     def get(self):
#         vals = {}
#         template = JINJA_ENVIRONMENT.get_template('landingpage.html')
#         self.response.write(template.render(vals))
#         genre_id = self.request.get('genre')
#         go = self.request.get("submitButton")
#         vals2 = {}
#         movies = [Movie(getMovieInfo(t=movie_title)) for movie_title in getMovie(genre_id=genre_id)]
#         vals2["movies"] = movies
#         template = JINJA_ENVIRONMENT.get_template('outputpage.html')
#         self.response.write(template.render(vals2))

# class MainHandler(webapp2.RequestHandler):
#     def get(self):
#         vals = {}
#         template = JINJA_ENVIRONMENT.get_template('test.html')
#         self.response.write(template.render(vals))
#         genre_id = self.request.get('username')
#         go = self.request.get("gobtn")
#         if genre_id:
#             vals2 = {}
#             movieList = getMovie(genre_id=genre_id)
#             movies = []
#             for movie in movieList:
#                 movies.append(Movie(getMovieInfo(t=movie)))
#             # movies = [Movie(getMovieInfo(t=title)) for title in getMovie(genre_id=genre_id)]
#             vals2["movies"] = movies
#             template = JINJA_ENVIRONMENT.get_template('outputpage.html')
#             self.response.write(template.render(vals2))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        vals = {}
        vals['page_title'] = "Moive Inspire Homepage"
        template = JINJA_ENVIRONMENT.get_template('landingpage.html')
        self.response.write(template.render(vals))

    def post(self):
        vals = {}
        vals['page_title'] = "Movie Inspire!"
        genre_id = self.request.get('genre')
        go = self.request.get("gobtn")
        logging.info(genre_id)
        logging.info(go)
        if genre_id:
            movieList = getMovie(genre_id=genre_id)
            movies = []
            for movie in movieList:
                if "Error" not in getMovieInfo(t=movie):
                    movies.append(Movie(getMovieInfo(t=movie)))
            # movies = [Movie(getMovieInfo(t=title)) for title in getMovie(genre_id=genre_id)]
            vals["movies"] = movies
            template = JINJA_ENVIRONMENT.get_template('outputpage.html')
            self.response.write(template.render(vals))
            logging.info('genre= '+genre_id)



# class MainHandler(webapp2.RequestHandler):
#     def get(self):
#         vals = {}
#         template = JINJA_ENVIRONMENT.get_template('landingpage.html')
#         self.response.write(template.render(vals))
#         genre_id = self.request.get('genre')
#         go = self.request.get("gobtn")
#         if genre_id:
#             vals2 = {}
#             movieList = getMovie(genre_id=genre_id)
#             movies = []
#             for movie in movieList:
#                 movies.append(Movie(getMovieInfo(t=movie)))
#             # movies = [Movie(getMovieInfo(t=title)) for title in getMovie(genre_id=genre_id)]
#             vals2["movies"] = movies
#             template = JINJA_ENVIRONMENT.get_template('outputpage.html')
#             self.response.write(template.render(vals2))


application = webapp2.WSGIApplication([('/', MainHandler), ('/results', MainHandler)], debug=True)

