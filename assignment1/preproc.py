from io import BytesIO
import sqlite3
from zipfile import ZipFile

import requests


def setup_database():
  """
  Load the MovieLens dataset into sqlite database. The function only needs to be
  called once.
  """
  # Download the data
  url = 'http://files.grouplens.org/datasets/movielens/ml-latest-small.zip'
  r = requests.get(url)
  zipfile = ZipFile(BytesIO(r.content))

  # ['ml-latest-small/', 'ml-latest-small/links.csv',
  # 'ml-latest-small/tags.csv', 'ml-latest-small/ratings.csv',
  # 'ml-latest-small/README.txt', 'ml-latest-small/movies.csv']

  conn = sqlite3.connect('assignment1.db')
  c = conn.cursor()

  # TODO any smarter schema design?
  # Create table
  c.execute('''CREATE TABLE links
                 (MovieId integer, ImdbId integer, TmdbId integer)''')
  # sqlite does not support array data type, hence in Genres the input will be
  # kept as the raw format - string value of "action|romance|<...>".
  c.execute('''CREATE TABLE movies
                 (MovieId integer, Title text, Year integer, Genres text)''')
  c.execute('''CREATE TABLE ratings
                 (UserId integer, MovieId integer, rating real, timestamp integer)
                 ''')
  c.execute('''CREATE TABLE tags
                 (MovieId integer, ImdbId integer, TmdbId integer,
                 timestamp integer)''')

  # links.csv
  # movieId,imdbId,tmdbId
  # 1,0114709,862
  for lineno, line in enumerate(
      zipfile.open('ml-latest-small/links.csv').readlines()):
    if lineno == 0:
      assert line.decode('utf-8').strip() == 'movieId,imdbId,tmdbId'
      continue
    c.execute('INSERT INTO links VALUES (?, ?, ?)',
              (*line.decode('utf-8').strip().split(','), ))

  # movies.csv
  # movieId,title,genres
  # 1,Toy Story (1995),Adventure|Animation|Children|Comedy|Fantasy
  for lineno, line in enumerate(
      zipfile.open('ml-latest-small/movies.csv').readlines()):
    if lineno == 0:
      assert line.decode('utf-8').strip() == 'movieId,title,genres'
      continue
    decoded = line.decode('utf-8').strip()
    # hack to clean some bad encoding
    decoded = decoded.replace(', The (', ' (')
    # split in three steps to avoid the movie names with comma
    movie_id, rest = decoded.split(',', 1)
    rest, genres = rest.rsplit(',', 1)
    try:
      title, year = rest.rsplit(' ', 1)
    except ValueError:
      # eg. 156605,Paterson,(no genres listed)
      title = rest
      year = 'null'  # if year not present, set to 'null'
    year = year[1:-1]
    c.execute('INSERT INTO movies VALUES (?, ?, ?, ?)',
              (movie_id, title, year, genres,))

  # tags.csv
  # userId,movieId,tag,timestamp
  # 2,60756,funny,1445714994
  for lineno, line in enumerate(
      zipfile.open('ml-latest-small/tags.csv').readlines()):
    if lineno == 0:
      assert line.decode('utf-8').strip() == 'userId,movieId,tag,timestamp'
      continue
    c.execute('INSERT INTO tags VALUES (?, ?, ?, ?)',
              (*line.decode('utf-8').strip().split(','),))

  conn.commit()
  conn.close()
