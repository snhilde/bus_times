#! /bin/python3.7

import json
import requests
import sys
import time

nt_url_base = "http://svc.metrotransit.org/NexTrip/"
    
def usage():
    print("Usage:")
    print("\tpybus {stop_id}")
    print("To get departure times for stop 123:")
    print("\tpybus 123")
    
def check_args():
    if len(sys.argv) != 2:
        usage()
        exit()
        
def get_minutes_left(timestamp:int, departure_str:str) -> int:
    time = departure_str.split('(')[1].split(')')[0].split('-')[0]
    departure_time = int(time) / 1000
    
    seconds_left = departure_time - timestamp
    
    return int(seconds_left / 60)
    
def get_stop_id() -> int:
    try:
        stop_id = int(sys.argv[1])
    except ValueError:
        usage()
        exit()
            
    return stop_id
        
def get_times(stop_id:int) -> json.loads:
    url = "{}{}?format=json".format(nt_url_base, stop_id)
    response = requests.get(url)
    
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None
    
def print_header(stop_id:int):
    print()
    print("Bus times for stop {}".format(stop_id))
    print()
    print("Current time: {}".format(time.strftime('%I:%M')))
    print()
    
def print_times(busses_json:json.loads):
    timestamp = time.time()
    
    for bus in busses_json:
        route = bus["Route"]
        departure_time = bus["DepartureText"]
        
        if bus["Actual"]:
            print("Rte {}: {}".format(route, departure_time))
        else:
            minutes_left = get_minutes_left(timestamp, bus["DepartureTime"])
            print("Rte {}: {} (Scheduled, {} min.)".format(route, departure_time, minutes_left))
    
def main():
    check_args()
    stop_id = get_stop_id()
        
    busses = get_times(stop_id)
    
    print_header(stop_id)
    print_times(busses)
        
if __name__ == '__main__':
    main()
