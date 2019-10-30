from py2neo import Graph, Node, Relationship

graph = Graph(password="password")

# print number of links by year
print("--- Number of LINKS by Year ---")
numLinksYear = graph.run("MATCH ()-[r:LINK]->() RETURN r.date.year as year,count(*) as count ORDER BY year")
print(numLinksYear.to_data_frame())

# number of links by post
print("--- Number of LINKS by Post ---")
numLinksPost = '''
    MATCH (s:Subreddit)-[r:LINK]->() RETURN r.post_id as post,count(*) as count ORDER BY count DESC LIMIT 10
'''
ex = graph.run(numLinksPost)
print(ex.to_data_frame())

''' Multigraphs '''
# eigenvector centrality algorithm 
print("--- Eigenvector Centrality ---")
eigen = '''
    CALL algo.eigenvector.stream('Subreddit','LINK')
    YIELD nodeId,score
    RETURN algo.getNodeById(nodeId).id as subreddit,score
    ORDER BY score DESC LIMIT 10
'''
e2 = graph.run(eigen)
print(e2.to_data_frame())

