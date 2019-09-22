import sqlite3
from io import BytesIO
import unicodedata
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
  # The genres are "expanded" into columns of ints (sqlite does not have
  # boolean type) to make the query faster (and make the database smaller).
  c.execute('''CREATE TABLE movies (
                 MovieId INTEGER PRIMARY KEY,
                 Title TEXT,
                 Year INTEGER,
                 Action INTEGER DEFAULT 0,
                 Adventure INTEGER DEFAULT 0,
                 Animation INTEGER DEFAULT 0,
                 Children INTEGER DEFAULT 0,
                 Comedy INTEGER DEFAULT 0,
                 Crime INTEGER DEFAULT 0,
                 Documentary INTEGER DEFAULT 0,
                 Drama INTEGER DEFAULT 0,
                 Fantasy INTEGER DEFAULT 0,
                 FilmNoir INTEGER DEFAULT 0,
                 Horror INTEGER DEFAULT 0,
                 Musical INTEGER DEFAULT 0,
                 Mystery INTEGER DEFAULT 0,
                 Romance INTEGER DEFAULT 0,
                 SciFi INTEGER DEFAULT 0,
                 Thriller INTEGER DEFAULT 0,
                 War INTEGER DEFAULT 0,
                 Western INTEGER DEFAULT 0
               )''')

  # ratings table
  c.execute('''CREATE TABLE ratings (
                 UserId INTEGER,
                 MovieId INTEGER,
                 Rating REAL,
                 Year INTEGER,
                 FOREIGN KEY(MovieId) REFERENCES movies(MovieId)
               )''')
  # Two join columns are indexed.
  c.execute('''CREATE INDEX ratings_UserId_index
               ON ratings(UserId)''')
  c.execute('''CREATE INDEX ratings_MovieId_index
               ON ratings(MovieId)''')
  # optimize for GROUP BY Rating
  c.execute('''CREATE INDEX ratings_Rating_index
               ON ratings(Rating)''')
  # optimize for GROUP BY Rating, Year
  c.execute('''CREATE INDEX ratings_Rating_Year_index
                 ON ratings(Rating, Year)''')
  # tags table
  c.execute('''CREATE TABLE tags (
                 UserId INTEGER,
                 MovieId INTEGER,
                 Tag TEXT,
                 Year INTEGER,
                 FOREIGN KEY (MovieId) REFERENCES movies(MovieId)
               )''')
  # Two join columns are indexed.
  c.execute('''CREATE INDEX tags_UserId_index
               ON tags(UserId)''')
  c.execute('''CREATE INDEX tags_MovieId_index
               ON tags(MovieId)''')
  # Since we are generating the word cloud for tags, it better be indexed.
  c.execute('''CREATE INDEX tags_Tag_index
               ON tags(tag)''')

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
    decoded = unicodedata.normalize('NFKD', decoded)
    # hack to clean some bad encoding
    decoded = decoded.replace(', The (', ' (')
    # split in three steps to avoid the movie names with comma
    movie_id, rest = decoded.split(',', 1)
    rest, genres = rest.rsplit(',', 1)
    genres = decode_genres(genres.split('|'))
    # eg: 96608,Runaway Brain (1995) ,Animation|Comedy|Sci-Fi
    # remove the trailing white space from the title-year part.
    rest = rest.strip(' ')
    # remove the opening and closing double quote, if present.
    if rest[0] == rest[-1] == '"':
      rest = rest[1:-1]
    # if the title-year does not end with ')', then year info is missing.
    # eg. 156605,Paterson,(no genres listed)
    if rest[-1] != ')':
      title = rest
      year = 'null'
    else:
      lb_idx = rest.rfind('(')
      title, year = rest[: lb_idx].strip(' '), rest[lb_idx + 1: -1]
      # some garbage data that I am too lazy to handle
      # eg 79607,"Millions Game, The (Das Millionenspiel)",Action|Drama|Sci-Fi
      if len(year) != 4:
        continue
    c.execute('''INSERT INTO movies VALUES (
                   ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                 )''',
              (movie_id, title, year, *genres,))

  # ratings.csv
  for lineno, line in enumerate(
      zipfile.open(dataset_name + '/ratings.csv').readlines()):
    if lineno == 0:
      assert line.decode('utf-8').strip() == 'userId,movieId,rating,timestamp'
      continue
    c.execute('''INSERT INTO ratings VALUES (
                   ?, ?, ?, substr(datetime(?, 'unixepoch'), 0, 5)
                 )''',
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


def decode_genres(genres: list):
  """
  Garbage fire. It stinks yet you don't want to touch it.
  """
  action = \
    adventure = \
    animation = \
    children = \
    comedy = \
    crime = \
    documentary = \
    drama = \
    fantasy = \
    film_noir = \
    horror = \
    musical = \
    mystery = \
    romance = \
    sci_fi = \
    thriller = \
    war = \
    western = 0
  for g in genres:
    if g == 'Action':
      action += 1
    if g == 'Adventure':
      adventure += 1
    if g == 'Animation':
      animation += 1
    if g == "Children's":
      children += 1
    if g == 'Comedy':
      comedy += 1
    if g == 'Crime':
      crime += 1
    if g == 'Documentary':
      documentary += 1
    if g == 'Drama':
      drama += 1
    if g == 'Fantasy':
      fantasy += 1
    if g == 'Film-Noir':
      film_noir += 1
    if g == 'Horror':
      horror += 1
    if g == 'Musical':
      musical += 1
    if g == 'Mystery':
      mystery += 1
    if g == 'Romance':
      romance += 1
    if g == 'Sci-Fi':
      sci_fi += 1
    if g == 'Thriller':
      thriller += 1
    if g == 'War':
      war += 1
    if g == 'Western':
      western += 1
  return action, adventure, animation, children, comedy, crime, documentary, \
         drama, fantasy, film_noir, horror, musical, mystery, romance, sci_fi, \
         thriller, war, western


if __name__ == '__main__':
  setup_database(dataset='S', mode='fetch')
