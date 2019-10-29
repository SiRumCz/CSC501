
### Basics  

The tab separated columns from soc-redditHyperlinks-body.tsv were put into a .csv file via Excel.  
The tab separated columns and some of the comma separated ones from soc-redditHyperlinks-title.tsv were as well.  
The comma separated columns that were added are the positive, negative and composite sentiments according to VADER.  
This .csv files are in this directory in the Imports folder titled 'body_tab_separated.csv' and 'title_tab_separated.csv'.

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
computer$ python load_data_body.py  
<py2neo.database.Cursor object at 0x1177ea8d0>  
  
            Source           Target       ID            Time  
0  leagueoflegends  teamredditteams  1u4nrps  12/31/13 16:39  
1       theredlion           soccer   1u4qkd  12/31/13 18:18  
2     inlandempire           bikela  1u4qlzs    1/1/14 14:54  
  
                Source  numCount  
0       subredditdrama      4665  
1          circlebroke      2358  
2      shitliberalssay      1968  
3         outoftheloop      1958  
4            copypasta      1824  
...                ...       ...  
27859         cockhero         1  
27860       soundcloud         1  
27861       daddyofive         1  
27862      mildlynomil         1  
27863             None         0  

[27864 rows x 2 columns]  
