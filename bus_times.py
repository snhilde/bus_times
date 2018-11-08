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
    print("\tbus_times {stop_id(s)}")
    print("To get sorted departure times for stops 123 and 456:")
    print("\tbus_times 123 456")
    
def check_args() -> list:
    stop_id_list = []
    
    for id in sys.argv[1:]:
        if stop_id_re.match(id):
            stop_id_list.append(id)
            
    if not stop_id_list:
        usage()
        exit()
                
    return stop_id_list
        
def get_minutes_left(timestamp:int, departure_str:str) -> int:
    time = departure_str.split('(')[1].split(')')[0].split('-')[0]
    departure_time = int(time) / 1000
    
    seconds_left = departure_time - timestamp
    
    return int(seconds_left / 60)
    
def get_times(stop_id_list:list) -> list:
    json_list = []
            
    for stop_id in stop_id_list:
        url = "{}{}?format=json".format(nt_url_base, stop_id)
        response = requests.get(url)
        
        if response.status_code == 200:
            json_list.append(json.loads(response.content.decode('utf-8')))
        else:
            print("Error getting times for stop {}".format(stop_id))
                
    return json_list
    
def print_header(stop_id_list:list):
    stop_id_string = ", ".join(stop_id_list)
    
    print("\nBus times for stop", end='')
    
    if len(stop_id_list) > 1:
        print("s", end='')
        
    print(" {}\n".format(stop_id_string))
    print("Current time: {}\n".format(time.strftime('%I:%M')))
    
def print_times(busses:list):
    timestamp = time.time()
    max_route_number_length = max(len(bus['Route']) for bus in busses)
    
    for bus in busses[:19]:
        route = bus["Route"]
        route = route + " " * (max_route_number_length - len(route))
        departure_time = bus["DepartureText"]
        
        if bus["Actual"]:
            print("Rte {}: {}".format(route, departure_time))
        else:
            minutes_left = get_minutes_left(timestamp, bus["DepartureTime"])
            print("Rte {}: {} (Scheduled, {} min.)".format(route, departure_time, minutes_left))
            
def sort_times(json_list:list) -> list:
    busses = [bus for busses_json in json_list for bus in busses_json]
    busses.sort(key=lambda x: x['DepartureTime'])
        
    return busses
    
def main():
    stop_id_list = check_args()
    json_list = get_times(stop_id_list)
    busses = sort_times(json_list)
    
    print_header(stop_id_list)
    print_times(busses)
        
if __name__ == '__main__':
    main()
