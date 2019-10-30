from py2neo import Graph, Node, Relationship
from timeit import default_timer as timer

from flask import Flask, jsonify
from flask import g as flask_globals
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def execute_query(query: str) -> list:
    if 'graph' not in flask_globals:
        flask_globals.graph = Graph(password="password")
    start = timer()
    ret_val = flask_globals.graph.run(query)
    app.logger.debug('query time: %f seconds', timer() - start)
    if ret_val is None:
        return list()
    return ret_val


@app.route('/links-per-year', methods=['GET'])
def links_by_year():
    """
    number of links by year.
    """
    query = ''' MATCH ()-[r:LINK]->() RETURN r.date.year as year,count(*) as count ORDER BY year '''
    result = execute_query(query)
    return jsonify([{'year': a[0], 'count': a[1]} for a in result])


@app.route('/top10-links-by-post', methods=['GET'])
def top_10_links_by_post():
    """
    number of links by post.
    """
    query = ''' MATCH (s:Subreddit)-[r:LINK]->() RETURN r.post_id as post,count(*) as count ORDER BY count DESC LIMIT 10 '''
    result = execute_query(query)
    return jsonify([{'post': a[0], 'count': a[1]} for a in result])


if __name__ == '__main__':
  app.debug = True
  app.run()