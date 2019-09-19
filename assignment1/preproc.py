import sqlite3
from io import BytesIO
from zipfile import ZipFile

import requests

DATASET = {
  'S': 'ml-latest-small',
  'L': 'ml-latest'
}


def setup_database(dataset: str, mode: str):
  """
  Load the MovieLens dataset into sqlite database. The function only needs to be
  called once.

  :param dataset: String value specify the dataset. Can be 'S' for
                  ml-latest-small.zip or 'L' for ml-latest.zip
  :param mode: String value specify fetch the dataset from URL or local storage.
               Can be 'fetch' or 'local'.
  """
  dataset_name = DATASET.get(dataset)
  assert dataset_name is not None, 'dataset arg not supported'
  if mode == 'fetch':
    url = 'http://files.grouplens.org/datasets/movielens/' \
          + dataset_name + '.zip'
    r = requests.get(url)
    zipfile = ZipFile(BytesIO(r.content))
  elif mode == 'local':
    zipfile = ZipFile(dataset_name + '.zip')
  else:
    raise ValueError('mode arg not supported')

  # ['ml-latest-small/', 'ml-latest-small/links.csv',
  # 'ml-latest-small/tags.csv', 'ml-latest-small/ratings.csv',
  # 'ml-latest-small/README.txt', 'ml-latest-small/movies.csv']

  conn = sqlite3.connect('assignment1.db')
  c = conn.cursor()

  # TODO any smarter schema design?
  # Create table

  # links table
  c.execute('''CREATE TABLE links (
                 MovieId INTEGER,
                 ImdbId INTEGER,
                 TmdbId INTEGER,
                 FOREIGN KEY (MovieId) REFERENCES movies(MovieId)
               )''')
  c.execute('''CREATE UNIQUE INDEX links_MovieId_index
               ON links(MovieId)''')

  # movies table
  # sqlite does not support array data type, hence in Genres the input will be
  # kept as the raw format - string value of "action|romance|<...>".
  c.execute('''CREATE TABLE movies (
                 MovieId INTEGER PRIMARY KEY,
                 Title TEXT,
                 Year INTEGER, 
                 Genres TEXT
               )''')
  # Genres will be used to search substring (LIKE in WHERE clause), hence
  # indexed.
  c.execute('''CREATE INDEX movies_Genres_index
               ON movies(Genres)''')

  # ratings table
  c.execute('''CREATE TABLE ratings (
                 UserId INTEGER,
                 MovieId INTEGER,
                 Rating REAL,
                 Timestamp TIMESTAMP,
                 FOREIGN KEY(MovieId) REFERENCES movies(MovieId)
               )''')
  # Two join columns are indexed.
  c.execute('''CREATE INDEX ratings_UserId_index
               ON ratings(UserId)''')
  c.execute('''CREATE INDEX ratings_MovieId_index
               ON ratings(MovieId)''')

  # tags table
  c.execute('''CREATE TABLE tags (
                 UserId INTEGER,
                 MovieId INTEGER,
                 Tag TEXT,
                 Timestamp TIMESTAMP,
                 FOREIGN KEY (MovieId) REFERENCES movies(MovieId)
               )''')
  # Two join columns are indexed.
  c.execute('''CREATE INDEX tags_UserId_index
               ON tags(UserId)''')
  c.execute('''CREATE INDEX tags_MovieId_index
               ON tags(MovieId)''')

  # links.csv
  # movieId,imdbId,tmdbId
  # 1,0114709,862
  for lineno, line in enumerate(
      zipfile.open(dataset_name + '/links.csv').readlines()):
    if lineno == 0:
      assert line.decode('utf-8').strip() == 'movieId,imdbId,tmdbId'
      continue
    c.execute('INSERT INTO links VALUES (?, ?, ?)',
              (*line.decode('utf-8').strip().split(','),))

  # movies.csv
  # movieId,title,genres
  # 1,Toy Story (1995),Adventure|Animation|Children|Comedy|Fantasy
  for lineno, line in enumerate(
      zipfile.open(dataset_name + '/movies.csv').readlines()):
    if lineno == 0:
      assert line.decode('utf-8').strip() == 'movieId,title,genres'
      continue
    decoded = line.decode('utf-8').strip()
    # hack to clean some bad encoding
    decoded = decoded.replace(', The (', ' (')
    # split in three steps to avoid the movie names with comma
    movie_id, rest = decoded.split(',', 1)
    rest, genres = rest.rsplit(',', 1)
    # remove the opening and closing double quote, if present.
    if rest[0] == rest[-1] == '"':
      rest = rest[1:-1]
    try:
      title, year = rest.rsplit(' ', 1)
    except ValueError:
      # eg. 156605,Paterson,(no genres listed)
      title = rest
      year = 'null'  # if year not present, set to 'null'
    year = year[1:-1]
    c.execute('INSERT INTO movies VALUES (?, ?, ?, ?)',
              (movie_id, title, year, genres,))

  # ratings.csv
  for lineno, line in enumerate(
      zipfile.open(dataset_name + '/ratings.csv').readlines()):
    if lineno == 0:
      assert line.decode('utf-8').strip() == 'userId,movieId,rating,timestamp'
      continue
    c.execute("INSERT INTO ratings VALUES (?, ?, ?, datetime(?, 'unixepoch'))",
              (*line.decode('utf-8').strip().split(','),))

  # tags.csv
  # userId,movieId,tag,timestamp
  # 2,60756,funny,1445714994
  for lineno, line in enumerate(
      zipfile.open(dataset_name + '/tags.csv').readlines()):
    if lineno == 0:
      assert line.decode('utf-8').strip() == 'userId,movieId,tag,timestamp'
      continue
    decoded = line.decode('utf-8').strip()
    # handle case where the tag has comma in it hence double quoted:
    # 449,2428,"Brilliant, but Lazy",1509119084
    user_id, movie_id, rest = decoded.split(',', 2)
    tag, timestamp = rest.rsplit(',', 1)
    if rest[0] == rest[-1] == '"':
      tag = tag[1:-1]
    c.execute("INSERT INTO tags VALUES (?, ?, ?, datetime(?, 'unixepoch'))",
              (user_id, movie_id, tag, timestamp))

  conn.commit()
  conn.close()
