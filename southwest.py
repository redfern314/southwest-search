import argparse
import cookielib
import itertools
import json
import sys
import tabulate
import time
from selenium import webdriver

# Airports that Southwest operates out of
cities = ['ABQ', 'ALB', 'AMA', 'ATL', 'AUA', 'AUS', 'BDL', 'BHM', 'BNA', 'BOI', 'BOS', 'BOT', 'BUF', 'BUR',
          'BWI', 'BZE', 'CAK', 'CHS', 'CLE', 'CLT', 'CMH', 'CNN', 'CRP', 'CUN', 'CVL', 'DAL', 'DAY', 'DCA',
          'DEN', 'DSM', 'DTW', 'ECP', 'ELP', 'EWR', 'FLL', 'FNT', 'GEG', 'GRR', 'GSP', 'HOU', 'HRL', 'IAD',
          'ICT', 'IND', 'ISP', 'JAX', 'LAS', 'LAX', 'LBB', 'LGA', 'LGB', 'LIR', 'LIT', 'LOS', 'MAF', 'MBJ',
          'MCI', 'MCO', 'MDW', 'MEM', 'MEX', 'MHT', 'MKE', 'MMA', 'MSP', 'MSY', 'NAS', 'NFB', 'NWY', 'OAK',
          'OKC', 'OMA', 'ONT', 'ORF', 'PBI', 'PDX', 'PHL', 'PHX', 'PIT', 'PNS', 'PUJ', 'PVD', 'PVR', 'PWM',
          'RDU', 'RIC', 'RNO', 'ROC', 'RSW', 'SAN', 'SAT', 'SDF', 'SEA', 'SFC', 'SFO', 'SJC', 'SJD', 'SJO',
          'SJU', 'SLC', 'SMF', 'SNA', 'STL', 'TPA', 'TUL', 'TUS', 'WDC']

def is_search_form(form):
    return form.attrs.get("class") == "swa-header--search-overlay"

def page_grab(d, date, depart, arrive):
    try:
        d.get("http://www.southwest.com/")
        time.sleep(1)

        d.find_elements_by_id("trip-type-one-way")[0].click()
        d.find_elements_by_id("air-city-departure")[0].clear()
        d.find_elements_by_id("air-city-departure")[0].send_keys(depart)
        d.find_elements_by_id("air-city-arrival")[0].clear()
        d.find_elements_by_id("air-city-arrival")[0].send_keys(arrive)
        d.find_elements_by_id("air-date-departure")[0].clear()
        d.find_elements_by_id("air-date-departure")[0].send_keys(date)
        d.find_elements_by_id("jb-booking-form-submit-button")[0].click()
    except Exception as e:
        print e

def page_parse(d, date, depart_city, arrive_city):
    options = []
    rows = d.find_elements_by_class_name("air-booking-select-detail")
    for flight in rows:
        try:
            option = {}
            option["date"] = date
            option["flight"] = flight.find_elements_by_class_name("flight-numbers--flight-number")[0].text
            option["depart"] = ""
            option["arrive"] = ""
            for t in flight.find_elements_by_class_name("air-operations-time-status"):
                if t.get_attribute("type") == "origination":
                    option["depart"] = t.text
                elif t.get_attribute("type") == "destination":
                    option["arrive"] = t.text
            option["fares"] = []
            for f in flight.find_elements_by_class_name("fare-button--value-total"):
                option["fares"].append(int(f.text))
            option["fares"].sort()
            stops = flight.find_elements_by_class_name("flight-stops--item")
            option["route"] = [depart_city]
            for s in stops:
                option["route"].append(s.text.split('\n')[0])
            option["route"].append(arrive_city)
            option["stops"] = len(option["route"])
            option["duration"] = flight.find_elements_by_class_name("flight-stops--duration-time")[0].text
            options.append(option)
        except Exception as e:
            print e

    return options


def pretty_print_flights(flights, sort, lowest_fare, max_stops, reverse):
    keys = ["flight", "date", "depart", "arrive", "fares", "route", "stops", "duration"]
    flight_list = []
    for flight in flights:
        if max_stops is not None and flight["stops"] > max_stops:
            continue

        if lowest_fare:
            flight["fares"] = min(flight["fares"])

        thisflight = []
        for key in keys:
            thisflight.append(flight[key])

        flight_list.append(thisflight)

    if sort is not None:
        flight_list.sort(key=lambda l: l[keys.index(sort)], reverse=reverse)
    print tabulate.tabulate(flight_list, headers=keys)

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--arrival-cities', action='store', nargs="+", required=True)
parser.add_argument('-d', '--departure-cities', action='store', nargs="+", required=True)
parser.add_argument('-t', '--dates', action='store', nargs="+", required=True)
parser.add_argument('-s', '--sort', action='store', choices=["flight", "depart", "arrive", "fares",
                    "stops", "duration"], help="Choose which column you want to sort results by.")
parser.add_argument('-r', '--reverse', action='store_true', help="Reverse sort order for key of choice.",
                    default=False)
parser.add_argument('-l', '--show-only-lowest-fare', action='store_true', help="Only shows the lowest fare " +
                    "for each route. (Usually a 'Wanna Get Away?' fare, but could be a different type.)")
parser.add_argument('-m', '--max-stops', type=int, help="Filter for flights with this many stops or less.")
parser.add_argument('-e', '--export-file', type=str, help="Save results to a file. Useful if you want to " +
                    "sort and filter the same results different ways without re-making the server requests.")
parser.add_argument('-i', '--import-file', type=str, help="Load results from a file create with --export.")

args = parser.parse_args(namespace=None)

for city in (args.arrival_cities + args.departure_cities):
    if city not in cities:
        print "Departure and arrival cities must be one of the following: %s" % cities
        sys.exit()

if args.import_file is not None:
    with open(args.import_file, "r") as f:
        options = json.load(f)
else:
    options = []
    i = 0
    possible = len(args.dates) * len(args.departure_cities) * len(args.arrival_cities)

    # init selenium
    config = webdriver.ChromeOptions()
    config.add_argument('headless')
    d = webdriver.Chrome(chrome_options=config)

    for route in itertools.product(args.dates, args.departure_cities, args.arrival_cities):
        try:
            page_grab(d, *route)
            time.sleep(5)
            options += page_parse(d, *route)
            i += 1
            print "Processed %i/%i" % (i, possible)
        except Exception as e:
            print e
            continue

    d.quit()

if args.export_file is not None:
    with open(args.export_file, "w") as f:
        json.dump(options, f)

pretty_print_flights(options, args.sort, args.show_only_lowest_fare, args.max_stops, args.reverse)
