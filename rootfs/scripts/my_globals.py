import os

DEBUG=True

internal_uri = os.getenv('URL')

local_sqlite_db_file = '/config/bike_speed/bike_data_2.db' if "HASSIO_TOKEN" in os.environ else 'S:\\\\bike_speed\\bike_data_2.db'

diameter = float(700)
circumference = float (diameter/1000)*3.1415
plateau = 42
pignon = 20
braket_ratio=plateau/pignon
circumference_per_braket_ratio = circumference*braket_ratio
ms_to_kmh=60*60/1000

g_hour = 0
g_minute = 1
g_second = 2
g_speed = 3
g_distance = 4
g_rowid = 5

global g_event_list
g_event_list = []

g_connector = {}
g_cursor = {}

g_app = None

def set_flask_app(app):
    global g_app
    g_app = app

def reset_event_list():
    global g_event_list
    tmp = []
    for e in g_event_list:
        tmp.append(e)
    for f in tmp:
        g_event_list.remove(f)
