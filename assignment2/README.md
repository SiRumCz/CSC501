# Assignment 2 folder

This project runs on Python 3.x and Node.js 12.x and latest Jupyter Notebook

## how to run backend server
1. download the both taxi-sample.zip from the connecx assignment page (https://connex.csc.uvic.ca/access/content/attachment/b81a868e-bf59-4c43-a1ff-7e18731eec86/Assignments/3b7d8dd7-5c45-4aea-b478-f0952040da10/taxi-sample.zip) and put them under this directory.
2. download the 112M 2018 Yellow Taxi Trip Data from (https://data.cityofnewyork.us/api/views/t29m-gskq/rows.csv?accessType=DOWNLOAD) and put them under this directory.
3. download the taxi zone lookup file from [official website](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page) or https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv and put them under this directory.
4. `pip install -r requirements.txt` to install any applicable dependencies.
5. run 'python setup_db.py' to process the raw data into usable sqlite database. This process will roughly take up to 3 to 4 hours. If you weish to skip this part and decide to use the existing database file, you can directly download it from https://drive.google.com/open?id=1POc_uU6bnQKImJsnsS5QQrdPVk5x01X0 .
6. once the `assignment2.db` file is created or downloaded, run `python app.py` to have server running locally. the address is using default settings (http://localhost:5000/).

## how to run frontend react application
1. redirect to `assignment2/visualization/assignment2-visualization-react`.
2. run `npm install` to install dependencies.
3. run `npm start` to have the application running in developer mode.
4. the application should direct you to a browser of the application, if it failed to do so, you can navigate to `http://localhost:3000/` to view our visualization.

## jupyter notebooks
1. to download the Python3 notebook and the associated files that were used to create many of the maps and videos for this assignment: https://drive.google.com/file/d/1JfZV8V-OODIqB2iCJ5dv1PDt8ZRZfvdD/view?usp=sharing
2. open jupyter notebook by either entering cli or clicking app icon
3. open the notebook files
4. after you open the notebook file, you will need to install all the libraries that the notebook imported.
5. simply rerun every code block to get visualizations.
