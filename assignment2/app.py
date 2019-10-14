import sqlite3
from timeit import default_timer as timer

from flask import Flask, jsonify
from flask import g as flask_globals
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def get_db():
  """
  Connect to the sqlite database.
  """
  if 'db' not in flask_globals:
    flask_globals.db = sqlite3.connect('assignment2.db')
  return flask_globals.db


def close_db(err=None):
  """
  Close the database connection.
  """
  db = flask_globals.pop("db", None)
  if db is not None:
    db.close()


def execute_query(query: str):
  if 'db' not in flask_globals:
    flask_globals.db = sqlite3.connect('assignment2.db')
  c = flask_globals.db.cursor()
  start = timer()
  ret_val = c.execute(query).fetchall()
  app.logger.debug('query time: %f seconds', timer() - start)
  return ret_val


@app.route('/test-api', methods=['GET'])
def api_check():
  """
  Dummy health check endpoint for front-end debugging (if necessary).
  """
  return jsonify({'success': True})


@app.route('/average-passenger-counts', methods=['GET'])
def avg_passenger_counts():
  """
  Average passenger counts for New York taxi pick-up areas.
  [
    {"aid": 1, "value": 2.03},
    {...},
    ...
  ]
  """
  query = ''' SELECT z.LocationID,
              ROUND(IFNULL(AVG(t.passenger_count), 0.0), 2) AS avg
              FROM zones z
              LEFT JOIN trips t
              ON (z.LocationID = t.PULocationID)
              GROUP BY z.LocationID
              ORDER BY z.LocationID;
          '''
  result = execute_query(query)
  return jsonify([{'areaId': a[0], 'avgPassengers': a[1]} for a in result])


@app.route('/rush-pickup-hours', methods=['GET'])
def rush_pickup_hours():
  """
  New York taxi pick-up rush hours.
  [
    {"time": "00:00", "trips": 34805},
    {...},
    ...
  ]
  """
  query = ''' WITH t1 AS (
              SELECT STRFTIME('%H:00', tpep_pickup_datetime) AS pickup_time
              FROM trips)
              SELECT pickup_time, COUNT(pickup_time) AS pickup_counts
              FROM t1
              GROUP BY pickup_time
              ORDER BY pickup_time; 
          '''
  result = execute_query(query) 
  return jsonify([{'time': a[0], 'pickups': a[1]} for a in result])


@app.route('/busy-areas', methods=['GET'])
def num_pickup_by_areas():
  """
  Number of pickup events for each taxi area in data periods.
  [
    {"areaId": 1, "pickups": 31},
    {...},
    ...
  ]
  """
  query = ''' SELECT z.LocationID, COUNT(*) AS trip_counts
              FROM zones z
              LEFT JOIN trips t 
              ON (z.LocationID = t.PULocationID)
              GROUP BY z.LocationID
              ORDER BY z.LocationID;
          '''
  result = execute_query(query) 
  return jsonify([{'areaId': a[0], 'pickups': a[1]} for a in result])


@app.route('/payment-trend-usage', methods=['GET'])
def payment_trend_usage():
  """
  How many times each payment method has been used during the data period.
  [
    {"paymentId": 1, "paymentType": "Credit card", "totalUsage": 622051},
    {...},
    ...
  ]
  """
  query = ''' SELECT p.paymentID, p.payment_type, COUNT(tpep_pickup_datetime) AS usage
              FROM payments p
              LEFT JOIN trips t
              ON (p.paymentID = t.payment_type)
              GROUP BY p.paymentID
              ORDER BY p.paymentID;
          '''
  result = execute_query(query) 
  return jsonify([{
    'paymentId': a[0], 
    'paymentType': a[1], 
    'totalUsage': a[2]} for a in result])


@app.route('/payment-trend-timeline', methods=['GET'])
def payment_trend_timeline():
  """
  From 2018-12-27 to 2019-09-09 in sample data, how often each payment type has 
  been used.
  """
  query = ''' WITH t1 AS (
              SELECT DATE(tpep_dropoff_datetime) AS dd,
              payment_type
              FROM trips)
              SELECT dd, payment_type, COUNT(dd) AS usage
              FROM t1
              GROUP BY dd, payment_type
              ORDER BY dd, payment_type;
          '''
  result = execute_query(query)
  payment_types = [
    {1: 'Credit card'},
    {2: 'Cash'},
    {3: 'No charge'},
    {4: 'Dispute'},
    {5: 'Unknown'},
    {6: 'Voided trip'}
    ]
  trends = []
  prevDate = None
  currPayment = 1
  for ptusage in result:
    date, payment_type, usage = ptusage
    if prevDate is None or date != prevDate:
      trends.append({
        'date': date, 'data': []
      })
      while(payment_type > currPayment):
        trends[-1]['data'].append({'paymentID': currPayment, 'usage': 0})
      trends[-1]['data'].append({'paymentID': payment_type, 'usage': usage})
      
  return


if __name__ == '__main__':
  app.debug = True
  app.teardown_appcontext(close_db)
  app.run()
