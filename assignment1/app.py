from collections import defaultdict
import sqlite3
from timeit import default_timer as timer

from flask_cors import CORS
from flask import Flask, jsonify
from flask import g as flask_globals

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


def ids_to_links(group: list):
  links = []
  for i in range(len(group)):
    for j in range(i+1, len(group)):
      links.append({"source": group[i], "target": group[j]})
  return links


def links_trim(existing_links: list, link_group: list):
  # TODO: link trims. Increment weight for any duplicate link
  return None


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


@app.route('/basic-node-link-v1', methods=['GET'])
def basic_nodelink_v1():
  """
  Weighted Genre link nodes.
  [
    {
      "links": [
        {
          "source": 1, 
          "target": 2
        }, 
        ... 
      ]
      "nodes": [
        {
          "group": 1, 
          "id": 0, 
          "name": "Action", 
          "value": 1828
        }, 
        ...
      ]
    }
  ]
  """
  node_keys = ["Action","Adventure","Animation","Children","Comedy","Crime",
    "Documentary","Drama","Fantasy","FilmNoir","Horror","Musical","Mystery",
    "Romance","SciFi","Thriller","War","Western"
  ]
  # how many times each genre has appeared
  node_weights_query = ''' 
              SELECT {}
              FROM movies '''.format('SUM('+'), SUM('.join(node_keys)+')')
  # genre links 
  links_query = ''' SELECT {} FROM movies '''.format(', '.join(node_keys))
  node_weights = execute_query(node_weights_query)[0]
  links_results = execute_query(links_query)
  nodes = []
  links = []
  for index in range(len(node_keys)):
    nodes.append(
      {
        "id": index,
        "name": node_keys[index],
        "value": node_weights[index]
      }
    )
  for link in links_results:
    valid_genre_ids = [i for i,v in enumerate(link) if v == 1]
    links.extend(ids_to_links(valid_genre_ids))
  return jsonify([{"nodes":nodes, "links": links}])


if __name__ == '__main__':
  app.debug = True
  app.teardown_appcontext(close_db)
  app.run()
