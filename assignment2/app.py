import sqlite3

from flask import Flask, jsonify
from flask import g as flask_globals
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def get_db():
  """
  Connect to the sqlite database.
  """
  if 'db' not in flask_globals:
    flask_globals.db = sqlite3.connect('assignment2.db')
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
    flask_globals.db = sqlite3.connect('assignment2.db')
  c = flask_globals.db.cursor()
  start = timer()
  ret_val = c.execute(query).fetchall()
  app.logger.debug('query time: %f seconds', timer() - start)
  return ret_val


@app.route('/test-api', methods=['GET'])
def api_check():
  """
  Dummy health check endpoint for front-end debugging (if necessary).
  """
  return jsonify({'success': True})





if __name__ == '__main__':
  app.debug = True
  app.teardown_appcontext(close_db)
  app.run()
