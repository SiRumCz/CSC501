
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
  
### Expected Output  

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
