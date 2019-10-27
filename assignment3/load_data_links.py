from py2neo import Graph, Node, Relationship
import pandas as pd 

''' insert your own password here - you can set it at localhost:7474 '''
graph = Graph(password="password")

''' create Subreddit1 that stores the tab separated data from sub_ex_title.csv file that was put on filebin '''
# query = '''
# USING PERIODIC COMMIT 
# LOAD CSV WITH HEADERS FROM 'https://filebin.net/24au1ydtmhymcwz4/sub_ex_title.csv?t=5tttaxwm' AS line
# CREATE (:Subreddit1 { SourceSub: line.SOURCE_SUBREDDIT, TargetSub: line.TARGET_SUBREDDIT, PostID: line.POST_ID, \
#   Timestamp: line.TIMESTAMP, Link_Sentiment: line.LINK_SENTIMENT, Pos_Vader: line.POS_SENT_VADER, \
#   Neg_Vader: line.NEG_SENT_VADER, Comp_Vader: line.COMP_SENT_VADER })
# '''
query = '''
USING PERIODIC COMMIT 
LOAD CSV WITH HEADERS FROM 'file:////title_tab_separated.csv' AS line
CREATE (:Subreddit1 { SourceSub: line.SOURCE_SUBREDDIT, TargetSub: line.TARGET_SUBREDDIT, PostID: line.POST_ID, \
  Timestamp: line.TIMESTAMP, Link_Sentiment: line.LINK_SENTIMENT, Pos_Vader: line.POS_SENT_VADER, \
  Neg_Vader: line.NEG_SENT_VADER, Comp_Vader: line.COMP_SENT_VADER })
'''
data = graph.run(query)
print(data)

# print Subreddit1 as a dataframe using .to_data_frame()
print()
print(graph.run("MATCH (a:Subreddit1) RETURN a.SourceSub as Source, a.TargetSub as Target, a.PostID as ID, a.Timestamp as Time, a.Link_Sentiment LIMIT 3").to_data_frame())


# order source subreddits by the number of times they appear
questions_teams_per_country = '''
MATCH (t:Subreddit1) RETURN DISTINCT t.SourceSub as Source, count(t.SourceSub) AS numCount ORDER BY numCount DESC;
'''
this = graph.run(questions_teams_per_country)
print()
print(this.to_data_frame())