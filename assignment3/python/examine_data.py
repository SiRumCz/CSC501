from py2neo import Graph, Node, Relationship
import sys
graph = Graph(password="password")

if (len(sys.argv) < 2):
    print("Missing argument - lpa, regular, eigenvector, eigenvector2 or pagerank")

elif (sys.argv[1]=="regular"):
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

    ''' Multigraph '''
elif (sys.argv[1]=="eigenvector"):
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

elif (sys.argv[1]=="eigenvector2"):
    # eigenvector centrality top 5 positive and negative 
    print("--- Top 5 Positive and Negative ---")
    eigen = '''
        UNWIND [-1, 1] as sentiment
        CALL algo.eigenvector.stream(
        'MATCH (s:Subreddit) return id(s) as id',
        'MATCH (s:Subreddit)-[r:LINK]->(t:Subreddit)
        // Use parameter
        WHERE r.link_sentiment = $sentiment
        // Deduplicate relationships
        WITH id(s) as source,id(t) as target,count(*) as count
        RETURN source,target',
        {graph:'cypher', params:{sentiment:sentiment}})
        YIELD nodeId,score
        WITH sentiment,algo.getNodeById(nodeId).id as id,score
        ORDER BY score DESC
        RETURN sentiment,collect(id)[..5] as top5
    '''
    e2 = graph.run(eigen)
    print(e2.to_data_frame())

    ''' Cypher Projection '''
elif (sys.argv[1]=="pagerank"):  
    # weighted pageRank
    print("--- Weighted PageRank ---")
    pageR = '''
        CALL algo.pageRank.stream(
        // Node statement
        'MATCH (s:Subreddit) RETURN id(s) as id',
        // Relationship statement
        'MATCH (s:Subreddit)-[:LINK]->(t:Subreddit)
        RETURN id(s) as source, id(t) as target, count(*) as weight',
        {graph:'cypher',weightProperty:'weight'})
        YIELD nodeId,score
        RETURN algo.getNodeById(nodeId).id as subreddit, score
        ORDER BY score DESC LIMIT 10
    '''
    e3 = graph.run(pageR)
    print(e3.to_data_frame())
elif (sys.argv[1]=="lpa"):
    # Label propagation algorithm for community detection
    print("--- Label Propagation ---")
    # return top 5 communities
    lpa = '''
    CALL algo.labelPropagation.stream(
        "Subreddit", "LINK",
        {direction: "OUTGOING", iterations: 10}) 
    YIELD nodeId, label
    RETURN label, count(*) as size, collect(algo.asNode(nodeId).id) 
    as subreddits 
    ORDER BY size DESC LIMIT 5
    '''
    e4 = graph.run(lpa)
    print(e4.to_data_frame())

