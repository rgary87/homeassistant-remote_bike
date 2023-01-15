from my_globals import *
from my_mqtt import *
from my_sqlite import *
import time, datetime

def cycling_data_gathering():
    while True:
        rots_per_second=0
        bike_speed=0
        bike_distance=0
        rotations = float(0)
        sample_duration = 10 # in seconds
        time.sleep(sample_duration)
        if len(g_event_list) > 0:
            rotations = len(g_event_list)
            reset_event_list()
            rots_per_second = float(rotations/sample_duration)
            bike_speed = float(rots_per_second * circumference_per_braket_ratio * ms_to_kmh) 
            bike_distance = rotations * circumference_per_braket_ratio
        write_data_to_sqlite(datetime.datetime.now(), bike_speed, bike_distance)

def main():
    print('HELLO IN BIKE REMOTE SPEED MAIN FUNCTION')
    init_sqlite()
    init_mqtt()
    cycling_data_gathering()

if __name__ == "__main__":
    print('HELLO IN BIKE SPEED APPLICATION')
    main()