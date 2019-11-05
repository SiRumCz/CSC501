import networkx as nx
from networkx.algorithms import community

from py2neo import Graph, Node, Relationship

from timeit import default_timer as timer

from flask import Flask, jsonify, request
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


def make_directed_graph(nodes: list, links: list) -> nx.DiGraph:
    """
    create networkx directional graph
    """
    start = timer()
    G = nx.DiGraph()
    G.add_nodes_from([(n['id'], n) for n in nodes])
    G.add_edges_from(links)
    app.logger.debug('directional graph created in {:0.2f} seconds'.format(timer() - start))
    return G


def eigenvector_centrality(G: nx.Graph, size: int) -> nx.Graph:
    """
    downsizing algorithm
    nodes are ranked by their influences in the network
    """
    start = timer()
    centrality = nx.eigenvector_centrality_numpy(G)
    app.logger.debug('eigenvector centrality score computed in {:0.2f} seconds'.format(timer() - start))
    ranked_list = sorted((c, v) for v, c in centrality.items())
    remove_nodes = [n for (s, n) in ranked_list[:len(G)-size]]
    G.remove_nodes_from(remove_nodes)
    return G
 

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


@app.route('/edge-bundling', methods=['GET'])
def edge_bundling_top_n():
    """
    edge bundling graph on top selected nodes
    API format: /edge-bundling?size=<number of nodes>
    @param size: top n number of nodes. default value is 100 
    [
        {'name': '48.pcmasterrace', 'size': 60, 'imports': ["0.personalfinance", "0.self", ...]},
        {...}
        ...
    ] 
    """
    size = request.args.get('size', default=100, type=int)
    get_nodes_query = '''
        MATCH (n:Subreddit)-[LINK]->(Subreddit)
        RETURN n.id AS id
    '''
    nodes_result = execute_query(get_nodes_query)
    get_links_query = '''
        MATCH (s)-[LINK]->(t) 
        RETURN s.id AS source, t.id AS target
    '''
    links_result = execute_query(get_links_query)
    # nx directional graph
    G = make_directed_graph(nodes=nodes_result, links=links_result)
    # downsizing using eigenvector centrality score
    ecs_G = eigenvector_centrality(G=G, size=size)
    # communities detection - label propagation algorithm
    communities_generator = community.asyn_lpa_communities(ecs_G)
    # update name attr
    for c in communities_generator:
        comm = list(c)
        for i, n in enumerate(comm):
            G.add_node(n, name=str(i)+'.'+str(n))
    # update size and imports attrs
    ret_nodes = list(G.nodes(data=True))
    for n in ret_nodes:
        (node, attrs) = n
        attrs['size'] = G.out_degree(node)
        attrs['imports'] = [nx.get_node_attributes(G, 'name')[t] for (s, t) in list(G.out_edges(node))]
    return jsonify([data for (n, data) in ret_nodes])


if __name__ == '__main__':
  app.debug = True
  app.run()