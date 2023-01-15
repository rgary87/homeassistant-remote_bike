from flask import Flask, request, abort, url_for, render_template
import time, os, datetime
from threading import Thread
from my_globals import *
from my_sqlite import *
import bike_remote_speed
app = Flask(__name__)

# hour = 0
# minute = 1
# second = 2
# speed = 3
# distance = 4

@app.route("/data_for_date", methods=['GET'])
def getDataForDate():
    date = request.args.get("date")
    if date is None:
        abort(404)
    if DEBUG: print(f'Date: {date}')
    f_underscore = date.index('_')
    s_underscore = date.index('_', f_underscore + 1)
    year = date[0:f_underscore]
    month = date[f_underscore + 1: s_underscore]
    day = date[s_underscore + 1:]
    return get_data_for_date(year, month, day)

@app.route("/")
def getDatesForTabs():
    if g_app == None: set_flask_app(app)
    if internal_uri is not None:
        return render_template('page.html', internal_uri=internal_uri, tabs=getDates())
    else:
        return render_template('page.html', tabs=getDates())

@app.route("/instant", methods=['GET'])
def instant_data():
    return get_instant_data_from_sqlite()

if __name__ == "__main__":
    print('HELLO IN MY SERVER APPLICATION')
    Thread(target=bike_remote_speed.main).start()
    app.run(host="0.0.0.0", port=8099, debug=True, use_evalex=False)

