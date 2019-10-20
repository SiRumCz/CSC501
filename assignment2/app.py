import sqlite3, datetime
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


@app.route('/average-passenger-counts-2018', methods=['GET'])
def avg_passenger_counts_2018():
  """
  Average passenger counts for New York taxi pick-up areas.
  [
    {"aid": 1, "value": 2.03},
    {...},
    ...
  ]
  """
  query = ''' SELECT * FROM temp_average_passenger_counts_2018; '''
  result = execute_query(query)
  return jsonify([{'areaId': a[0], 'avgPassengers': a[1]} for a in result])


@app.route('/pickup-rush-hours', methods=['GET'])
def pickup_rush_hours():
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


@app.route('/pickup-rush-hours-2018', methods=['GET'])
def pickup_rush_hours_2018():
  """
  New York taxi pick-up rush hours.
  [
    {"time": "00:00", "trips": 34805},
    {...},
    ...
  ]
  """
  query = ''' SELECT * FROM temp_pickup_rush_hours_2018; '''
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


@app.route('/busy-areas-2018', methods=['GET'])
def num_pickup_by_areas_2018():
  """
  Number of pickup events for each taxi area in data periods.
  [
    {"areaId": 1, "pickups": 31},
    {...},
    ...
  ]
  """
  query = ''' SELECT * FROM temp_busy_areas_2018; '''
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


@app.route('/payment-trend-usage-2018', methods=['GET'])
def payment_trend_usage_2018():
  """
  How many times each payment method has been used during the data period.
  [
    {"paymentId": 1, "paymentType": "Credit card", "totalUsage": 622051},
    {...},
    ...
  ]
  """
  query = ''' SELECT * FROM temp_payment_trend_usage_2018; '''
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
  [
    {
      "data": [
          {"paymentID": 1, "usage": 123856},
          {...},
          ...
        ],
        "date": "2018-12-27"
    },
    {...},
    ...
  ]
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
  trends = []
  prev_date = None
  prev_payment = 0
  # processing data
  for ptusage in result:
    date, payment_type, usage = ptusage
    # new date
    if prev_date is None or date != prev_date:
      # complete last date data
      if len(trends) != 0:
        while(prev_payment < 6):
          trends[-1]['data'].append({'paymentID': prev_payment+1, 'usage': 0})
          prev_payment += 1
      # complete missing date
      if prev_date is not None:
        prev_date_dt = datetime.datetime.strptime(prev_date, '%Y-%m-%d').date() + datetime.timedelta(days=1)
        curr_date_dt = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        while(curr_date_dt > prev_date_dt):
          trends.append({
            'date': prev_date_dt.strftime('%Y-%m-%d'), 'data': [
              {'paymentID': 1, 'usage': 0},
              {'paymentID': 2, 'usage': 0},
              {'paymentID': 3, 'usage': 0},
              {'paymentID': 4, 'usage': 0},
              {'paymentID': 5, 'usage': 0},
              {'paymentID': 6, 'usage': 0},
            ]
          })
          prev_date_dt += datetime.timedelta(days=1)
      trends.append({
        'date': date, 'data': []
      })
      prev_payment = 0
    # complete missing payments 
    while(payment_type > prev_payment+1):
      if (prev_payment == 0):
        prev_payment = 1
      trends[-1]['data'].append({'paymentID': prev_payment, 'usage': 0})
      prev_payment += 1
    # add current payment
    trends[-1]['data'].append({'paymentID': payment_type, 'usage': usage})
    prev_date = date
    prev_payment = payment_type
  # complete last data
  if (len(trends[-1]['data']) != 6):
    while(prev_payment < 6):
      trends[-1]['data'].append({'paymentID': prev_payment+1, 'usage': 0})
      prev_payment += 1
  return jsonify(trends)


@app.route('/payment-trend-timeline-2018', methods=['GET'])
def payment_trend_timeline_2018():
  """
  From 2018 Jan to Dec, how often each payment type has been used.
  [
    {
      "data": [
          {"paymentID": 1, "usage": 123856},
          {...},
          ...
        ],
        "month": 1
    },
    {...},
    ...
  ]
  """
  query = ''' SELECT * FROM temp_payment_trend_timeline_2018; '''
  result = execute_query(query)
  trends = []
  prev_month = None
  prev_payment = 0
  # processing data
  for ptusage in result:
    month, payment_type, usage = ptusage
    # new month
    if prev_month is None or month != prev_month:
      # complete last data
      if len(trends) != 0:
        while(prev_payment < 6):
          trends[-1]['data'].append({'paymentID': prev_payment+1, 'usage': 0})
          prev_payment += 1
      trends.append({
        'month': int(month), 'data': []
      })
      prev_payment = 0
    # complete missing payments 
    while(payment_type > prev_payment+1):
      if (prev_payment == 0):
        prev_payment = 1
      trends[-1]['data'].append({'paymentID': prev_payment, 'usage': 0})
      prev_payment += 1
    # add current payment
    trends[-1]['data'].append({'paymentID': payment_type, 'usage': usage})
    prev_month = month
    prev_payment = payment_type
  # complete last data
  if (len(trends[-1]['data']) != 6):
    while(prev_payment < 6):
      trends[-1]['data'].append({'paymentID': prev_payment+1, 'usage': 0})
      prev_payment += 1
  return jsonify(trends)


if __name__ == '__main__':
  app.debug = True
  app.teardown_appcontext(close_db)
  app.run()
