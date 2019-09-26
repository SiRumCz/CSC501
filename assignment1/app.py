import math
from collections import defaultdict
import sqlite3
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
  flask_globals.db.create_function('log10', 1, math.log10)
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
    flask_globals.db = get_db()
  c = flask_globals.db.cursor()
  start = timer()
  ret_val = c.execute(query).fetchall()
  app.logger.debug('query time: %f seconds', timer() - start)
  return ret_val


def ids_to_links(group: list) -> list:
  links = []
  # i: source node, j: target node
  for i in range(len(group)):
    for j in range(i+1, len(group)):
      links.append((group[i], group[j]))
  return links


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
  query = '''SELECT count(DISTINCT UserId) as Cnt, Tag FROM tags
             GROUP BY tag
             ORDER BY cnt DESC
             LIMIT 100'''
  result = execute_query(query)
  return jsonify([{'tag': t, 'count': cnt} for cnt, t in result])


@app.route('/tags-wordcloud-v2', methods=['GET'])
def tags_wordcloud_v2():
  total = execute_query('SELECT count(DISTINCT UserId) FROM tags')[0][0]
  query = '''SELECT count(DISTINCT MovieId) *
                      log10( count(DISTINCT UserId)*1.0 / {total} ) as weight,
                      Tag
               FROM tags
               GROUP BY Tag
               ORDER BY weight DESC
               LIMIT 50'''.format(total=total)
  result = execute_query(query)
  return jsonify([{'tag': t, 'count': weight} for weight, t in result])


@app.route('/top-5-rated-movies-each-genres', methods=['GET'])
def top_five_rated_movies_each_genres():
  """
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
    'genre': 'SciFi'
  },
  { 'data': [ { 'avgRating': 4.173971387139363,
                'movie': 'Pulp Fiction',
                'numRatings': 92406,
                'scale': 0.22705348433211542,
                'year': 1994},
              ...
            ],
    'genre': 'Thriller'
  },
  ...
  ]
  """
  genres = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime',
            'Documentary', 'Drama', 'Fantasy', 'FilmNoir', 'Horror', 'Musical',
            'Mystery', 'Romance', 'SciFi', 'Thriller', 'War', 'Western']
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
      "data": [{"movie": row[1], "year": row[2], "avgRating": row[3],
                "numRatings": row[4], "scale": row[4] / subtotal} for row in
               result]
    })
  return jsonify(ret_val)


@app.route('/basic-node-link-v1', methods=['GET'])
def basic_nodelink_v1():
  """
  Weighted Genre link nodes.
    {
      "links": [
        {
          "source": 1, 
          "target": 2,
          "weight": 247
        }, 
        ... 
      ]
      "nodes": [
        {
          "id": 0, 
          "name": "Action", 
          "value": 1828
        }, 
        ...
      ]
    }
  """
  node_keys = ["Action","Adventure","Animation","Children","Comedy","Crime",
    "Documentary","Drama","Fantasy","FilmNoir","Horror","Musical","Mystery",
    "Romance","SciFi","Thriller","War","Western"
  ]
  # how many times each genre has appeared
  basic_query = ''' SELECT {} FROM movies '''
  node_weights_query = basic_query.format('SUM('+'), SUM('.join(node_keys)+')')
  # genre links 
  genres_query = basic_query.format(', '.join(node_keys))
  node_weights = execute_query(node_weights_query)[0]
  genres_results = execute_query(genres_query)
  nodes = []
  raw_links = []
  # list to store existing links for duplicate filtering
  for index in range(len(node_keys)):
    nodes.append(
      {
        "id": index,
        "name": node_keys[index],
        "value": node_weights[index]
      }
    )
  for genres in genres_results:
    valid_genre_ids = [i for i,v in enumerate(genres) if v == 1]
    genre_links = ids_to_links(valid_genre_ids)
    for link in genre_links:
      link = tuple(sorted(link))
      # check existence of current link
      # return link index if True, otherwise return None
      link_index = next((i for i,l in enumerate(raw_links) if link in l), None)
      if link_index is None:
        raw_links.append({link: 1})
      else:
        raw_links[link_index][link] += 1
  # reformate links
  links = []
  for raw_link in raw_links:
    for link_tuple,link_weight in raw_link.items():
      links.append({
        "source": link_tuple[0],
        "target": link_tuple[1],
        "weight": link_weight
        })
  return jsonify({"nodes":nodes, "links": links})


if __name__ == '__main__':
  app.debug = True
  app.teardown_appcontext(close_db)
  app.run()
