from py2neo import Graph, Node, Relationship
import pandas as pd 

''' insert your own password here - you can set it at localhost:7474 '''
graph = Graph(password="password")

''' read the .tsv into panda '''
# data_rider = pd.read_csv('https://snap.stanford.edu/data/soc-redditHyperlinks-body.tsv')
# print(data_rider.head(3))
# print(list(data_rider))

''' create Subreddit2 that stores the tab separated data from the csv file that was put on filebin '''
query = '''
USING PERIODIC COMMIT 
LOAD CSV WITH HEADERS FROM 'https://filebin.net/jjba8brdv6uk8v5a/sub_ex.csv?t=4h0ygld8' AS line
CREATE (:Subreddit2 { SourceSub: line.SOURCE_SUBREDDIT, TargetSub: line.TARGET_SUBREDDIT, PostID: line.POST_ID, Timestamp: line.TIMESTAMP})
'''
data = graph.run(query)
print(data)

# print Subreddit2 as a dataframe using .to_data_frame()
print()
print(graph.run("MATCH (a:Subreddit2) RETURN a.SourceSub as Source, a.TargetSub as Target, a.PostID as ID, a.Timestamp as Time LIMIT 3").to_data_frame())


# order source subreddits by the number of times they appear
questions_teams_per_country = '''
MATCH (t:Subreddit2) RETURN DISTINCT t.SourceSub as Source, count(t.SourceSub) AS numCount ORDER BY numCount DESC;
'''
this = graph.run(questions_teams_per_country)
print()
print(this.to_data_frame())

