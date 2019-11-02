
### Basics  

To load the data you must put the soc-redditHyperlinks-title.tsv file in the imports folder.  
Inside of the Docker preferences in the advanced tab the memory needs to be increased to 4.0 GB.  
This code is loading the links file into neo4j and creating a LINK between source and target subreddits.   
Run examine_data.py after load_data.py.   

### Run neo4j in Docker   

cd assignment3  

docker-compose build  

docker-compose up neo4j  
  
### Navigate to localhost:7474 

use ':server connect' to start connection  
set password - default password is 'neo4j'  
make sure the password is the same as in load_data.py (password: password)  
to change password use ':server change-password' at localhost:7474  
  
### Expected Output - load_data.py

computer$ cd python  
computer$ python load_data.py 
<py2neo.database.Cursor object at 0x109a0d160>  

--- Number of LINKS by Year ---  
   year   count  
0  2013      27  
1  2014  128345  
2  2015  175096  
3  2016  194287  
4  2017   74172  

### Expected Output - examine_data.py  
#### Options: regular, pagerank, eigenvector

computer$ examine_data.py regular  
--- Number of LINKS by Year ---  
   year   count  
0  2013      27  
1  2014  128345  
2  2015  175096  
3  2016  194287  
4  2017   74172  
--- Number of LINKS by Post ---  
      post  count  
0  3na5zus      2  
1  4adtxws      2  
2  3oz3jos      2  
3  2m4lpis      2  
4  35ff4ss      2  
5   3fpbpp      1  
6  4jtcn2s      1  
7  1u4pzzs      1  
8  56dhwqs      1  
9  5bm3zgs      1  

computer$ examine_data.py pagerank  
--- Weighted PageRank ---  
       subreddit       score  
0           iama  561.132538  
1      askreddit  516.726707  
2           pics  287.035156  
3          funny  272.117404  
4         videos  222.036789  
5     the_donald  187.153909  
6         gaming  169.333164  
7          music  155.687642  
8  todayilearned  152.445091  
9      worldnews  150.822555  

computer$ examine_data.py eigenvector  
--- Eigenvector Centrality ---  
subreddit score  
0 iama 321.911086  
1 askreddit 311.323265  
2 pics 263.799529  
3 funny 258.084657  
4 videos 253.007776  
5 todayilearned 231.063511  
6 worldnews 184.428278  
7 gaming 182.708345  
8 news 180.482415  
9 gifs 165.655387  

computer$ examine_data.py eigenvector2  
--- Top 5 Positive and Negative ---  
   sentiment                                         top5  
0          1       [iama, askreddit, pics, funny, videos]  
1         -1  [askreddit, pics, worldnews, videos, funny]  

### To view a graph example  

navigate to localhot:7474  

MATCH path=(s:Subreddit)-[l:LINK]->()  
WHERE s.id = "canada" and l.link_sentiment = -1 and l.date.year = 2015  
RETURN path LIMIT 10  

### Shortest path

MATCH path = allShortestPaths(
     (u:Subreddit {id:"canada"})-[*]-(me:Subreddit {id:"ubc"}))
RETURN path;

MATCH path = shortestPath(
     (u:Subreddit {id:"mapporn"})-[*]-(me:Subreddit {id:"alpharetta"}))
RETURN path;