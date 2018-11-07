#! /bin/python3.7

import json
import re
import requests
import sys
import time

stop_id_re = re.compile('^\d{2,5}$')
nt_url_base = "http://svc.metrotransit.org/NexTrip/"

def usage():
    print("Usage:")
    print("\tpybus {stop_id}")
    print("To get departure times for stop 123:")
    print("\tpybus 123")
    
def check_args() -> list:
    stop_id_list = []
    
    if len(sys.argv) == 1:
        usage()
        exit()
        
    for id in sys.argv[1:]:
        if stop_id_re.match(id):
            stop_id_list.append(id)
            
    return stop_id_list
        
def get_minutes_left(timestamp:int, departure_str:str) -> int:
    time = departure_str.split('(')[1].split(')')[0].split('-')[0]
    departure_time = int(time) / 1000
    
    seconds_left = departure_time - timestamp
    
    return int(seconds_left / 60)
    
def get_times():
    for stop_id in stop_id_list:
        url = "{}{}?format=json".format(nt_url_base, stop_id)
        response = requests.get(url)
        
        if response.status_code == 200:
            json_list.append(json.loads(response.content.decode('utf-8')))
        else:
            print("Error getting times for stop {}".format(stop_id))
    
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
    stop_id_list = check_args()
    get_times()
    sort_times()
    
    #  print_header(stop_id)
    #  print_times(busses)
        
if __name__ == '__main__':
    main()
