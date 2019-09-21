import sqlite3
from collections import defaultdict

from flask import Flask, jsonify
from flask import g as flask_globals

app = Flask(__name__)


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
  return c.execute(query).fetchall()


@app.route('/health', methods=['GET'])
def health_check():
  """
  Dummy health check endpoint for front-end debugging (if necessary).
  """
  return {'success': True}


@app.route('/num-movies-by-ratings', methods=['GET'])
def num_movies_by_ratings():
  """
  Number of movies per ratings. [{rating:3.5, counts:114}, {...}, ...]
  """
  query = '''SELECT COUNT(*), Rating FROM ratings GROUP BY Rating'''
  result = execute_query(query)
  return jsonify([
    {'rating': rating, 'counts': counts} for rating, counts in result
  ])


@app.route('/rating-distribution-per-year', methods=['GET'])
def rating_distribution_per_year():
  """
  Number of movies per ratings per rating year.
  [
    {
      data: [{rating:3.5, counts:114}, {...}, ...],
      year: 2015
    }
    ...
  ]
  """
  # TODO: in preproc.py split the data instead of here. I don't think we need
  # finer resolution than Year (or month).
  query = '''SELECT COUNT(*), Rating, Year FROM ratings GROUP BY Rating, Year'''
  result = execute_query(query)
  temp = defaultdict(list)
  for rating, counts, year in result:
    temp[year].append({'rating': rating, 'counts': counts})
  return jsonify([{'data': v, 'year': k} for k, v in temp.items()])


@app.route('/genres-distribution-per-year', methods=['GET'])
def genres_distribution_per_year():
  """
  Number of movies per distribution per rating year.
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


if __name__ == '__main__':
  app.debug = True
  app.teardown_appcontext(close_db)
  app.run()