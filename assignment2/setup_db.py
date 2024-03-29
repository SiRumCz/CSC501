import sqlite3, csv

from datetime import datetime
from zipfile import ZipFile

DATASET = {
    'taxi' : 'taxi-sample',
    '2018_taxi' : '2018_Yellow_Taxi_Trip_Data.csv',
    'zones' : 'taxi+_zone_lookup.csv'
}


def setup_2018_taxi():
    """
    112M raw 2018 yellow taxi trip dataset pre processing
    """
    # connect db
    conn = sqlite3.connect('assignment2.db')
    c = conn.cursor()
    # create tables
    # table trips
    print('creating table trips_non_sample ...')
    c.execute(''' DROP TABLE IF EXISTS trips_non_sample; ''')
    c.execute('''
    CREATE TABLE trips_non_sample (
        VendorID int,
        tpep_pickup_datetime timestamp,
        tpep_dropoff_datetime timestamp,
        passenger_count int,
        trip_distance real,
        RatecodeID int,
        store_and_fwd_flag int,
        PULocationID int,
        DOLocationID int,
        payment_type int,
        fare_amount real,
        extra real,
        mta_tax real,
        tip_amount real,
        tolls_amount real,
        improvement_surcharge real,
        total_amount real,
        FOREIGN KEY (RatecodeID) REFERENCES ratecodes(ratecodeID),
        FOREIGN KEY (PULocationID) REFERENCES zones(LocationID),
        FOREIGN KEY (DOLocationID) REFERENCES zones(LocationID),
        FOREIGN KEY (payment_type) REFERENCES payments(paymentID)
    );
    ''')
    count = 0
    for lineno, line in enumerate(
        open(DATASET.get('2018_taxi'), 'r').readlines()):
        if lineno == 0:
            assert line.strip() == 'VendorID,tpep_pickup_datetime,tpep_dropoff_datetime,passenger_count,trip_distance,RatecodeID,store_and_fwd_flag,PULocationID,DOLocationID,payment_type,fare_amount,extra,mta_tax,tip_amount,tolls_amount,improvement_surcharge,total_amount'
            continue
        decoded = line.strip()
        val_list = decoded.split(',')
        val_list[1:] = [x.strip('\"') for x in val_list[1:]]
        val_list[1] = datetime.strptime(val_list[1], '%m/%d/%Y %I:%M:%S %p')
        val_list[2] = datetime.strptime(val_list[2], '%m/%d/%Y %I:%M:%S %p')
        if val_list[6] == 'N':
            val_list[6] = 0
        else:
            val_list[6] = 1
        count += 1
        if count % 500000 == 0:
            print(count)
        c.execute('INSERT INTO trips_non_sample VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', val_list)
    print(' Done!')
    
    # indexing
    c.execute(''' CREATE INDEX trips_ratecode_id_index ON trips_non_sample(RatecodeID); ''')
    c.execute(''' CREATE INDEX trips_pu_location_id_index ON trips_non_sample(PULocationID); ''')
    c.execute(''' CREATE INDEX trips_do_location_id_index ON trips_non_sample(DOLocationID); ''')
    c.execute(''' CREATE INDEX trips_payment_type_index ON trips_non_sample(payment_type); ''')
    
    conn.commit()
    conn.close()

def filter_2018_trips():
    # connect db
    conn = sqlite3.connect('assignment2.db')
    c = conn.cursor()
    # original count
    c.execute(''' SELECT COUNT(*) FROM trips_non_sample; ''')
    raw_count = c.fetchone()[0]
    print('total data size: {}'.format(raw_count))

    # filter data with datetime range from 2018-Jan to 2018-Dec
    print('filtering dataset down to period 2018 Jan to Dec ...', end='')
    c.execute(
        '''
        DELETE FROM trips_non_sample 
        WHERE (tpep_pickup_datetime NOT BETWEEN DATETIME('2018-01-01') AND DATETIME('2019-01-01'))
        OR (tpep_dropoff_datetime NOT BETWEEN DATETIME('2018-01-01') AND DATETIME('2019-01-01'));
        '''
    )
    print('Done!')

    print('removing duplicate data ...', end='')
    c.execute(''' 
    DELETE FROM trips_non_sample 
    WHERE rowid NOT IN (
        SELECT MIN(rowid)
        FROM trips_non_sample
        GROUP BY VendorID,
        tpep_pickup_datetime,
        tpep_dropoff_datetime,
        passenger_count,
        trip_distance,
        RatecodeID,
        store_and_fwd_flag,
        PULocationID,
        DOLocationID,
        payment_type,
        fare_amount,
        extra,
        mta_tax,
        tip_amount,
        tolls_amount,
        improvement_surcharge,
        total_amount
        ) ''')
    print(' Done!')

    c.execute(''' SELECT COUNT(*) FROM trips_non_sample; ''')
    filtered_count = c.fetchone()[0]
    print('{} filtered !'.format(raw_count - filtered_count))
    conn.commit()
    conn.close()


def setup_database():
    """
    20M taxi-sample dataset pre processing
    """
    taxi_trips_file = DATASET.get('taxi')
    taxi_zf = ZipFile(taxi_trips_file+'.zip')

    # connect db
    conn = sqlite3.connect('assignment2.db')
    c = conn.cursor()

    # create tables
    # table trips
    c.execute(''' DROP TABLE IF EXISTS trips; ''')
    c.execute('''
    CREATE TABLE trips (
        VendorID int,
        tpep_pickup_datetime timestamp,
        tpep_dropoff_datetime timestamp,
        passenger_count int,
        trip_distance real,
        RatecodeID int,
        store_and_fwd_flag int,
        PULocationID int,
        DOLocationID int,
        payment_type int,
        fare_amount real,
        extra real,
        mta_tax real,
        tip_amount real,
        tolls_amount real,
        improvement_surcharge real,
        total_amount real,
        FOREIGN KEY (RatecodeID) REFERENCES ratecodes(ratecodeID),
        FOREIGN KEY (PULocationID) REFERENCES zones(LocationID),
        FOREIGN KEY (DOLocationID) REFERENCES zones(LocationID),
        FOREIGN KEY (payment_type) REFERENCES payments(paymentID)
    );
    ''')

    # table zones : zones look up
    c.execute(''' DROP TABLE IF EXISTS zones; ''')
    c.execute('''
    CREATE TABLE zones (
        LocationID int PRIMARY KEY,
        Borough text,
        Zone text,
        service_zone text
    )
    ''')

    # table ratecodes
    print('creating table ratecodes ...', end='')
    c.execute(''' DROP TABLE IF EXISTS ratecodes; ''')
    c.execute('''
    CREATE TABLE ratecodes (
        ratecodeID int PRIMARY KEY,
        rate_type text
    )
    ''')
    ratecodes = [
        [1, 'Standard rate'],
        [2, 'JFK'],
        [3, 'Newark'],
        [4, 'Nassau or Westchester'],
        [5, 'Negotiated fare'],
        [6, 'Group ride']
    ]
    for rate in ratecodes:
        c.execute(''' INSERT INTO ratecodes VALUES(?,?) ''', rate)
    print(' Done!')

    # table payments
    print('creating table payments ...', end='')
    c.execute(''' DROP TABLE IF EXISTS payments; ''')
    c.execute('''
    CREATE TABLE payments (
        paymentID int PRIMARY KEY,
        payment_type text
    )
    ''')
    payments = [
        [1, 'Credit card'],
        [2, 'Cash'],
        [3, 'No charge'],
        [4, 'Dispute'],
        [5, 'Unknown'],
        [6, 'Voided trip']
    ]
    for payment in payments:
        c.execute(''' INSERT INTO payments VALUES(?,?) ''',payment)
    print(' Done!')

    # inserting dataset
    print('creating table trips ...', end='')
    for lineno, line in enumerate(
        taxi_zf.open('taxi-sample.csv').readlines()):
        if lineno == 0:
            assert line.decode('utf-8').strip() == 'VendorID,tpep_pickup_datetime,tpep_dropoff_datetime,passenger_count,trip_distance,RatecodeID,store_and_fwd_flag,PULocationID,DOLocationID,payment_type,fare_amount,extra,mta_tax,tip_amount,tolls_amount,improvement_surcharge,total_amount'
            continue
        decoded = line.decode('utf-8').strip()
        val_list = decoded.split(',')
        val_list[1] = datetime.strptime(val_list[1], '%m/%d/%Y %I:%M:%S %p')
        val_list[2] = datetime.strptime(val_list[2], '%m/%d/%Y %I:%M:%S %p')
        if val_list[6] == 'N':
            val_list[6] = 0
        else:
            val_list[6] = 1
        c.execute('INSERT INTO trips VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', val_list)
    print(' Done!')

    print('creating table zones ...', end='')
    for lineno, line in enumerate(
        open(DATASET.get('zones'), 'r').readlines()):
        if lineno == 0:
            assert line.strip() == '\"LocationID\",\"Borough\",\"Zone\",\"service_zone\"'
            continue
        decoded = line.strip()
        val_list = decoded.split(',')
        val_list[1:] = [x.strip('\"') for x in val_list[1:]]
        c.execute('INSERT INTO zones VALUES (?, ?, ?, ?)', val_list)
    print(' Done!')

    # remove duplicate data
    c.execute(''' SELECT COUNT(*) FROM trips; ''')
    raw_count = c.fetchone()[0]
    print('removing duplicate data ...', end='')
    c.execute(''' 
    DELETE FROM trips 
    WHERE rowid NOT IN (
        SELECT MIN(rowid)
        FROM trips
        GROUP BY VendorID,
        tpep_pickup_datetime,
        tpep_dropoff_datetime,
        passenger_count,
        trip_distance,
        RatecodeID,
        store_and_fwd_flag,
        PULocationID,
        DOLocationID,
        payment_type,
        fare_amount,
        extra,
        mta_tax,
        tip_amount,
        tolls_amount,
        improvement_surcharge,
        total_amount
        ) ''')
    print(' Done!')
    
    # remove data with invalid date
    print('removing invalid data ...', end='')
    c.execute(''' 
    DELETE FROM trips 
    WHERE tpep_pickup_datetime > DATETIME('now')
    OR tpep_dropoff_datetime > DATETIME('now');
    ''')
    print(' Done!')

    c.execute(''' SELECT COUNT(*) FROM trips; ''')
    filtered_count = c.fetchone()[0]

    print('{filtered} trips data filtered.'.format(filtered=raw_count-filtered_count))
    # indexing
    c.execute(''' CREATE INDEX trips_ratecode_id_index ON trips(RatecodeID); ''')
    c.execute(''' CREATE INDEX trips_pu_location_id_index ON trips(PULocationID); ''')
    c.execute(''' CREATE INDEX trips_do_location_id_index ON trips(DOLocationID); ''')
    c.execute(''' CREATE INDEX trips_payment_type_index ON trips(payment_type); ''')

    conn.commit()
    conn.close()


def create_temp_data():
    """
    temporary tables for original 112M large dataset
    """
    # connect db
    conn = sqlite3.connect('assignment2.db')
    c = conn.cursor()
    # /average-passenger-counts
    print('creating /average-passenger-counts temp table')
    c.execute('''
    CREATE TABLE temp_average_passenger_counts_2018 AS
        SELECT z.LocationID,
        ROUND(IFNULL(AVG(t.passenger_count), 0.0), 2) AS avg
        FROM zones z
        LEFT JOIN trips_non_sample t
        ON (z.LocationID = t.PULocationID)
        GROUP BY z.LocationID
        ORDER BY z.LocationID;
    ''')
    # /pickup-rush-hours
    print('creating /pickup-rush-hours temp table')
    c.execute('''
    CREATE TABLE temp_pickup_rush_hours_2018 AS
        WITH t1 AS (
            SELECT STRFTIME('%H:00', tpep_pickup_datetime) AS pickup_time
            FROM trips_non_sample)
        SELECT pickup_time, COUNT(pickup_time) AS pickup_counts
        FROM t1
        GROUP BY pickup_time
        ORDER BY pickup_time; 
    ''')
    # /busy-areas
    print('creating /busy-areas temp table')
    c.execute('''
    CREATE TABLE temp_busy_areas_2018 AS
        SELECT z.LocationID, COUNT(*) AS trip_counts
        FROM zones z
        LEFT JOIN trips_non_sample t 
        ON (z.LocationID = t.PULocationID)
        GROUP BY z.LocationID
        ORDER BY z.LocationID;
    ''')
    # /payment-trend-usage
    print('creating /payment-trend-usage temp table')
    c.execute('''
    CREATE TABLE temp_payment_trend_usage_2018 AS
        SELECT p.paymentID, p.payment_type, COUNT(tpep_pickup_datetime) AS usage
        FROM payments p
        LEFT JOIN trips_non_sample t
        ON (p.paymentID = t.payment_type)
        GROUP BY p.paymentID
        ORDER BY p.paymentID;
    ''')
    # /payment-trend-timeline
    print('creating /payment-trend-timeline temp table')
    c.execute('''
    CREATE TABLE temp_payment_trend_timeline_2018 AS
        WITH t1 AS (
            SELECT STRFTIME('%m', tpep_dropoff_datetime) AS month,
            payment_type
            FROM trips_non_sample)
        SELECT month, payment_type, COUNT(month) AS usage
        FROM t1
        GROUP BY month, payment_type
        ORDER BY month, payment_type;
    ''')
    # /payment-trend-timeline
    print('creating /interval-tree-passengers-2018 temp table')
    c.execute('''
    CREATE TABLE temp_interval_tree_passengers_2018 AS
        SELECT passenger_count, 
        STRFTIME('%m',MIN(tpep_pickup_datetime)) AS from_dt, 
        STRFTIME('%m',MAX(tpep_pickup_datetime)) AS to_dt 
        FROM trips_non_sample
        GROUP BY passenger_count
        ORDER BY passenger_count;
    ''')
    conn.commit()
    conn.close()


def drop_2018_taxi_data():
    # connect db
    conn = sqlite3.connect('assignment2.db')
    c = conn.cursor()
    print('dropping 2018 112M data from database')
    c.execute(''' DROP TABLE IF EXISTS trips_non_sample; ''')
    print('executing sqlite vacuum;')
    c.execute(''' vacuum; ''') # shrink db file
    conn.commit()
    conn.close()

    
if __name__ == '__main__':
    setup_database()
    setup_2018_taxi()
    filter_2018_trips()
    create_temp_data()
    drop_2018_taxi_data()
