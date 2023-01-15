import sqlite3
import datetime, time
import threading
from my_globals import *

# #######################################################
# #######################################################
# ####################   WRITE DATA   ###################
# #######################################################
# #######################################################
def init_sqlite():
    g_connector[threading.get_ident()] = sqlite3.connect(local_sqlite_db_file)
    g_cursor[threading.get_ident()] = g_connector[threading.get_ident()].cursor()
    try:
        g_cursor[threading.get_ident()].execute('CREATE TABLE IF NOT EXISTS bike_data(year INTEGER, month INTEGER, day INTEGER, hour INTEGER, minute INTEGER, second INTEGER, speed REAL, distance REAL)')
        res = g_cursor[threading.get_ident()].execute('SELECT COUNT(*) FROM bike_data').fetchone()[0]
        print(f'bike_data count: {res}')
    except Exception as e:
        print(f'{e}')
    try:
        g_cursor[threading.get_ident()].execute('CREATE TABLE IF NOT EXISTS bike_instant_data(timestamp REAL)')
        res = g_cursor[threading.get_ident()].execute('SELECT COUNT(*) FROM bike_instant_data').fetchone()[0]
        print(f'bike_instant_data count: {res}')
    except Exception as e:
        print(f'{e}')


def write_data_to_sqlite(data_time: datetime.datetime, speed: float, distance: float) -> None:
    check_connection_for_thread()
    insert = f"INSERT INTO bike_data VALUES ({data_time.year},{data_time.month},{data_time.day},{data_time.hour},{data_time.minute},{data_time.second},{speed:.2f},{distance:.2f})"
    g_cursor[threading.get_ident()].execute(insert)
    g_connector[threading.get_ident()].commit()


def write_instant_data_to_sqlite(rotation: int) -> None:
    check_connection_for_thread()
    if rotation != 0:
        g_cursor[threading.get_ident()].execute(f"INSERT INTO bike_instant_data VALUES ({round(time.time())})")
        g_connector[threading.get_ident()].commit()

            


# #######################################################
# #######################################################
# ##################   RETRIEVE DATA   ##################
# #######################################################
# #######################################################
def get_data_for_date(year, month, day):
    check_connection_for_thread()
    if DEBUG: print(f'Got {year} - {month} - {day}')
    res = g_cursor[threading.get_ident()].execute(f'SELECT hour, minute, second, speed, distance, rowid FROM bike_data WHERE year = {year} AND month = {month} AND day = {day}')
    totals = {}
    day_data = []
    res = res.fetchall()
    for i in range(1, len(res)-1):
        if float(res[i][g_speed]) == 0:
            if float(res[i-1][g_speed]) == 0 and float(res[i+1][g_speed]) == 0:
                continue
        val = res[i]
        if float(res[i-1][g_speed]) == 0 or float(res[i+1][g_speed]) == 0:
            day_data.append({'rowid': val[5], 'hour': val[0],'minute': val[1],'second':  val[2],'speed': val[3],'distance': val[4]})
        else:
            day_data.append({'rowid': val[5], 'hour': '','minute': '','second':  '','speed': val[3],'distance': val[4]})
    total_distance = g_cursor[threading.get_ident()].execute(f'SELECT SUM(distance) FROM bike_data WHERE year = {year} AND month = {month} AND day = {day}').fetchone()
    totals['total_distance'] = total_distance
    totals['data'] = day_data
    return totals


def get_instant_data_from_sqlite():
    check_connection_for_thread()
    bike_speed = 0
    bike_distance = 0
    time_diff = 5
    res = g_cursor[threading.get_ident()].execute(f"SELECT count(*) FROM bike_instant_data WHERE timestamp > {round((time.time() - time_diff))}")
    rotations = res.fetchall()[0][0]

    rots_per_second = float(rotations/time_diff)
    bike_speed = float(rots_per_second * circumference_per_braket_ratio * ms_to_kmh) 
    bike_distance = rotations * circumference_per_braket_ratio
    
    return {'speed': bike_speed, 'distance':bike_distance, 'time': time_diff}



def getDates():
    check_connection_for_thread()
    current_datetime = datetime.datetime.now()
    if DEBUG: print('kikoo')
    if current_datetime.day < 10:
        if DEBUG: print('current_datetime.day < 10')
        res = g_cursor[threading.get_ident()].execute(f"""SELECT distinct year, month, day FROM bike_data 
            WHERE
                year = {current_datetime.year} 
                AND ( (month = {current_datetime.month} AND day <= {current_datetime.day})
                OR (month = {current_datetime.month - 1} AND day >= {30 - current_datetime.day} ))
                ORDER BY month || day DESC""")
    else:
        if DEBUG: print('else')
        res = g_cursor[threading.get_ident()].execute(f"""SELECT distinct year, month, day FROM bike_data 
            WHERE
                year = {current_datetime.year} 
                AND month = {current_datetime.month}
                AND day >= {current_datetime.day - 10}
                ORDER BY month DESC, day DESC""")
    res = res.fetchall()
    if DEBUG: print(f'fetched {res}')
    dates = []
    for val in res:
        dates.append(f"{val[0]}_{val[1] if len(str(val[1])) == 2 else '0'+str(val[1])}_{val[2] if len(str(val[2])) == 2 else '0'+str(val[2])}")
        if DEBUG: print(f'val: {val}')
    return dates


def check_connection_for_thread():
    if threading.get_ident() not in g_connector:
        init_sqlite()