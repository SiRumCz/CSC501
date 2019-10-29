from py2neo import Graph, Node, Relationship

''' insert your own password here - you can set it at localhost:7474 '''
graph = Graph(password="password")

index1 = '''
CREATE INDEX ON :Subreddit1(SourceSub);
'''

index2 = '''
CREATE INDEX ON :Subreddit2(TargetSub);
'''

index3 = '''
CREATE INDEX ON :Subreddit2(SourceSub);
'''

data1 = graph.run(index1)
print(data1)

data2 = graph.run(index2)
print(data2)

data4 = graph.run(index3)
print(data4)

relation = '''
MATCH (a:Subreddit1),(b:Subreddit2) WHERE a.SourceSub = b.SourceSub CREATE (a)-[:TARGETS]->(b);
'''

data3 = graph.run(relation)
print(data3)
