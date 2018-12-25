import argparse
import itertools
import json
import re
import requests
import sys
import tabulate
import time
from datetime import datetime, timedelta

# Airports that Southwest operates out of
cities = ['ABQ', 'ALB', 'AMA', 'ATL', 'AUA', 'AUS', 'BDL', 'BHM', 'BNA', 'BOI', 'BOS', 'BOT', 'BUF', 'BUR',
          'BWI', 'BZE', 'CAK', 'CHS', 'CLE', 'CLT', 'CMH', 'CNN', 'CRP', 'CUN', 'CVL', 'DAL', 'DAY', 'DCA',
          'DEN', 'DSM', 'DTW', 'ECP', 'ELP', 'EWR', 'FLL', 'FNT', 'GEG', 'GRR', 'GSP', 'HOU', 'HRL', 'IAD',
          'ICT', 'IND', 'ISP', 'JAX', 'LAS', 'LAX', 'LBB', 'LGA', 'LGB', 'LIR', 'LIT', 'LOS', 'MAF', 'MBJ',
          'MCI', 'MCO', 'MDW', 'MEM', 'MEX', 'MHT', 'MKE', 'MMA', 'MSP', 'MSY', 'NAS', 'NFB', 'NWY', 'OAK',
          'OKC', 'OMA', 'ONT', 'ORF', 'PBI', 'PDX', 'PHL', 'PHX', 'PIT', 'PNS', 'PUJ', 'PVD', 'PVR', 'PWM',
          'RDU', 'RIC', 'RNO', 'ROC', 'RSW', 'SAN', 'SAT', 'SDF', 'SEA', 'SFC', 'SFO', 'SJC', 'SJD', 'SJO',
          'SJU', 'SLC', 'SMF', 'SNA', 'STL', 'TPA', 'TUL', 'TUS', 'WDC']

API_URL = "https://www.southwest.com/api/air-booking/v1/air-booking/page/air/booking/shopping"
API_KEY = "l7xx944d175ea25f4b9c903a583ea82a1c4c"


def page_grab(date, depart, arrive):
    payload = {"originationAirportCode":depart,
               "destinationAirportCode":arrive,
               "returnAirportCode":"",
               "departureDate":date,
               "departureTimeOfDay":"ALL_DAY",
               "returnDate":"",
               "returnTimeOfDay":"ALL_DAY",
               "adultPassengersCount":"1",
               "seniorPassengersCount":"0",
               "fareType":"USD",
               "passengerType":"ADULT",
               "tripType":"oneway",
               "promoCode":"",
               "reset":"true",
               "redirectToVision":"true",
               "int":"HOMEQBOMAIR",
               "leapfrogRequest":"true",
               "application":"air-booking",
               "site":"southwest"}
    headers = {
        'content-type': "application/json",
        'x-api-key': API_KEY,
        'cache-control': "no-cache",
    }

    response = requests.request("POST", API_URL, data=json.dumps(payload), headers=headers)

    if response.ok:
        return json.loads(response.text)
    else:
        return {}

def page_parse(data):
    if (data is {}) or (not data['success']):
        return []

    flights = data['data']['searchResults']['airProducts'][0]['details']
    parsed = []
    date_pattern = re.compile("([0-9]{4}-[0-9]{2}-[0-9]{2})T([0-9]{2}:[0-9]{2}).*")

    for flight in flights:
        option = {}

        option['fares'] = []
        for fare in flight['fareProducts']['ADULT'].values():
            if fare['availabilityStatus'] == 'AVAILABLE':
                option['fares'].append(fare['fare']['totalFare']['value'])
        if len(option['fares']) == 0:
            # no availability on this flight
            continue
        option['fares'].sort()

        option['flight'] = "/".join(flight["flightNumbers"])
        option['date'] = date_pattern.match(flight['departureDateTime']).group(1)
        option['route'] = [flight['originationAirportCode']]
        for stop in flight['stopsDetails']:
            option['route'].append(stop['destinationAirportCode'])
        option['depart'] = date_pattern.match(flight['departureDateTime']).group(2)
        option['arrive'] = date_pattern.match(flight['arrivalDateTime']).group(2)
        option['stops'] = len(flight['stopsDetails']) - 1
        hours = flight['totalDuration'] / 60
        minutes = flight['totalDuration'] % 60
        option['duration'] = "%02i:%02i" % (hours, minutes)

        parsed.append(option)

    return parsed

def pretty_print_flights(flights, sort, lowest_fare, max_stops, reverse, verbose):
    keys = ["flight", "date", "depart", "arrive", "fares", "route", "stops", "duration"]
    flight_list = []
    for flight in flights:
        if max_stops is not None and flight["stops"] > max_stops:
            continue

        # round to the nearest dollar
        for i in range(len(flight["fares"])):
          flight["fares"][i] = int(round(float(flight["fares"][i])))

        if lowest_fare:
            flight["fares"] = min(flight["fares"])

        flight["route"] = "-".join(flight["route"])

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
parser.add_argument('-t', '--dates', action='store', nargs="+", required=True, help="")
parser.add_argument('-s', '--sort', action='store', choices=["flight_num", "depart", "arrive", "fares",
                    "num_stops", "flight_time"], help="Choose which column you want to sort results by.")
parser.add_argument('-r', '--reverse', action='store_true', help="Reverse sort order for key of choice.",
                    default=False)
parser.add_argument('-l', '--show-only-lowest-fare', action='store_true', help="Only shows the lowest fare " +
                    "for each route. (Usually a 'Wanna Get Away?' fare, but could be a different type.)")
parser.add_argument('-m', '--max-stops', type=int, help="Filter for flights with this many stops or less.")
parser.add_argument('-e', '--export-file', type=str, help="Save results to a file. Useful if you want to " +
                    "sort and filter the same results different ways without re-making the server requests.")
parser.add_argument('-i', '--import-file', type=str, help="Load results from a file create with --export.")
parser.add_argument('-v', '--verbose', action='store_true', help="Display verbose info about stops. This is" +
                    " usually only helpful to distinguish between stops where you change planes and stops " +
                    "where you don't have to get off the plane.")

args = parser.parse_args(namespace=None)

for city in (args.arrival_cities + args.departure_cities):
    if city not in cities:
        print "Departure and arrival cities must be one of the following: %s" % cities
        sys.exit()

date_re = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}")
for date in args.dates:
    if date_re.match(date) is None:
        print "Dates must be in YYYY-MM-DD form"
        sys.exit()

if args.import_file is not None:
    with open(args.import_file, "r") as f:
        options = json.load(f)
else:
    options = []
    i = 0
    possible = len(args.dates) * len(args.departure_cities) * len(args.arrival_cities)

    for route in itertools.product(args.dates, args.departure_cities, args.arrival_cities):
        try:
            page = page_grab(*route)
            options += page_parse(page)
            i += 1
            print "Processed %i/%i" % (i, possible)
            if i < possible:
                # do not decrease this - avoids putting undue strain on SW's servers
                time.sleep(2)
        except Exception as e:
            print e
            continue

if args.export_file is not None:
    with open(args.export_file, "w") as f:
        json.dump(options, f)

pretty_print_flights(options, args.sort, args.show_only_lowest_fare, args.max_stops, args.reverse,
                     args.verbose)
