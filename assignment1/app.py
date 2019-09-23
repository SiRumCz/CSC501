import heapq
import pprint
import sqlite3
from collections import defaultdict
from timeit import default_timer as timer

from flask import Flask, jsonify
from flask import g as flask_globals
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def get_db():
  """
  Connect to the database.
  """
  if 'db' not in flask_globals:
    flask_globals.db = sqlite3.connect('assignment1.db')
  return flask_globals.db


def close_db(err=None):
  """
  Close the database connection.
  """
  db = flask_globals.pop("db", None)
  if db is not None:
    db.close()


def execute_query(query: str):
  if 'db' not in flask_globals:
    flask_globals.db = sqlite3.connect('assignment1.db')
  c = flask_globals.db.cursor()
  start = timer()
  ret_val = c.execute(query).fetchall()
  app.logger.debug('query time: %f seconds', timer() - start)
  return ret_val


@app.route('/health', methods=['GET'])
def health_check():
  """
  Dummy health check endpoint for front-end debugging (if necessary).
  """
  return {'success': True}


@app.route('/num-movies-by-ratings', methods=['GET'])
def num_movies_by_ratings():
  """
  Number of movies per ratings. On 27M dataset it takes ~ 2s. This query need to
  be optimized on 1B dataset.
  [
    {rating:3.5, counts:114},
    {...},
    ...
  ]
  """
  query = '''SELECT COUNT(*), Rating FROM ratings GROUP BY Rating'''
  result = execute_query(query)
  return jsonify([
    {'rating': rating, 'counts': counts} for rating, counts in result
  ])


@app.route('/rating-distribution-each-year', methods=['GET'])
def rating_distribution_each_year():
  """
  Number of movies per rating per rating year. The time (year) is when the
  movies are rated (other than when the movies are released). On 27M dataset it
  takes ~ 3s. This query need to be optimized on 1B dataset.
  [
    {
      data: [
        {rating:3.5, counts:114},
        {...},
        ...
      ],
      year: 2015
    }
    ...
  ]
  """
  query = '''SELECT COUNT(*), Rating, Year FROM ratings GROUP BY Rating, Year'''
  result = execute_query(query)
  temp = defaultdict(list)
  for rating, counts, year in result:
    temp[year].append({'rating': rating, 'counts': counts})
  return jsonify([{'data': v, 'year': k} for k, v in temp.items()])


@app.route('/genres-distribution-per-year', methods=['GET'])
def genres_distribution_per_year():
  """
  Number of movies per genres per year. The time (year) is when the movies are
  released. On 27M dataset it takes ~ 0.1s.
  [
    {
      data: [{genres:Action, counts:114}, {...}, ...],
      year: 2015
    }
    ...
  ]
  """
  query = '''SELECT SUM(Action), SUM(Adventure), SUM(Animation), SUM(Children),
               SUM(Comedy), SUM(Crime), SUM(Documentary), SUM(Drama),
               SUM(Fantasy), SUM(FilmNoir), SUM(Horror), SUM(Musical),
               SUM(Mystery), SUM(Romance), SUM(SciFi), SUM(Thriller), SUM(War),
               SUM(Western), Year
             FROM movies
             GROUP BY Year'''
  result = execute_query(query)
  temp = defaultdict(list)
  for *sums, year in result:
    temp[year].append({'Action': sums[0],
                       'Adventure': sums[1],
                       'Animation': sums[2],
                       'Children': sums[3],
                       'Comedy': sums[4],
                       'Crime': sums[5],
                       'Documentary': sums[6],
                       'Drama': sums[7],
                       'Fantasy': sums[8],
                       'FilmNoir': sums[9],
                       'Horror': sums[10],
                       'Musical': sums[11],
                       'Mystery': sums[12],
                       'Romance': sums[13],
                       'SciFi': sums[14],
                       'Thriller': sums[15],
                       'War': sums[16],
                       'Western': sums[17]})
  return jsonify([{'data': v, 'year': k} for k, v in temp.items()])


@app.route('/tags-wordcloud', methods=['GET'])
def tags_wordcloud():
  """
  Top 100 unique tags with the corresponding counts. On 27M dataset it takes
  ~ 0.1s.
  [
    {tag: 'classic', count: 9876},
    {...},
    ...
  ]
  """
  query = '''SELECT count(*) as Cnt, Tag FROM tags
             GROUP BY tag
             ORDER BY cnt DESC
             LIMIT 100'''
  result = execute_query(query)
  return jsonify([{'tag': t, 'count': cnt} for cnt, t in result])


@app.route('/basic-link-node-diagram', methods=['GET'])
def basic_link_node_diagram():
  """
  API for the basic node link diagram. The master node is the genre and the
  slave nodes are the top 5 most popular rated movies. Only the top 5 most rated
  genres are returned.

  For each node (master and slave), a scaling factor, |scale| is also provided
  for the front end to determine the size of each node.

  All the |scale| of the master nodes sum to 1, and within each master node,
  the |scale| of slave nodes sum to 1.

  [
  { 'data': [ { 'avgRating': 4.149695428470046,
                'movie': 'Matrix',
                'numRatings': 84545,
                'scale': 0.22566033908438674,
                'year': 1999},
              { 'avgRating': 4.120454684348836,
                'movie': 'Star Wars: Episode IV - A New Hope',
                'numRatings': 81815,
                'scale': 0.21837365476597198,
                'year': 1977},
              ...
            ],
    'genre': 'SciFi',
    'numMovies': 4740199,
    'scale': 0.06398958962782558
  },
  { 'data': [ { 'avgRating': 4.173971387139363,
                'movie': 'Pulp Fiction',
                'numRatings': 92406,
                'scale': 0.22705348433211542,
                'year': 1994},
              ...
            ],
    'genre': 'Thriller',
    'numMovies': 7489619,
    'scale': 0.10110496337364008
  },
  ...
  ]
  """
  genres = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime',
            'Documentary', 'Drama', 'Fantasy', 'FilmNoir', 'Horror', 'Musical',
            'Mystery', 'Romance', 'SciFi', 'Thriller', 'War', 'Western']
  # TODO: have a num_ratings_per_genre table.
  # First calculate the number of movies per genre, and the portion.
  num_movies_per_genre = dict()
  for genre in genres:
    num_movies_per_genre[genre] = execute_query('''
       SELECT sum(NumRatings)
       FROM rating_stats
       INNER JOIN movies ON movies.MovieId = rating_stats.MovieId
       WHERE movies.{genre} = 1'''.format(genre=genre))[0][0]
  total_num_movies = sum(v for v in num_movies_per_genre.values())
  # key: genre, value: portion of the movies in this genre out of the total.
  scale_per_genre = {k: v / total_num_movies for k, v in
                     num_movies_per_genre.items()}
  query_template = '''
  SELECT movies.MovieId, Title, Year, AvgRating, NumRatings
  FROM movies
  INNER JOIN rating_stats ON movies.MovieId == rating_stats.MovieId
  WHERE movies.{genre} = 1
  ORDER BY NumRatings DESC
  LIMIT 5
  '''
  query_result = {g: execute_query(query_template.format(genre=g)) for g in
                  genres}
  ret_val = []
  for genre, result in query_result.items():
    subtotal = sum(row[4] for row in result)
    ret_val.append({
      "genre": genre,
      "numRatings": num_movies_per_genre[genre],
      "scale": scale_per_genre[genre],
      "data": [{"movie": row[1], "year": row[2], "avgRating": row[3],
                "numRatings": row[4], "scale": row[4] / subtotal} for row in
               result]
    })
  top_n = heapq.nlargest(5, ret_val, key=lambda x: x['numRatings'])
  if app.debug:
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(top_n)
  return jsonify(top_n)


if __name__ == '__main__':
  app.debug = True
  app.teardown_appcontext(close_db)
  app.run()
