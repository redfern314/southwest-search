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
cities = ['ABQ', 'ALB', 'AMA', 'ATL', 'AUA', 'AUS', 'BDL', 'BHM', 'BNA', 'BOI', 'BOS', 'BOT', 'BUF',
          'BUR', 'BWI', 'BZE', 'CAK', 'CHS', 'CLE', 'CLT', 'CMH', 'CNN', 'CRP', 'CUN', 'CVL', 'DAL',
          'DAY', 'DCA', 'DEN', 'DSM', 'DTW', 'ECP', 'ELP', 'EWR', 'FLL', 'FNT', 'GEG', 'GRR', 'GSP',
          'HOU', 'HRL', 'IAD', 'ICT', 'IND', 'ISP', 'JAX', 'LAS', 'LAX', 'LBB', 'LGA', 'LGB', 'LIR',
          'LIT', 'LOS', 'MAF', 'MBJ', 'MCI', 'MCO', 'MDW', 'MEM', 'MEX', 'MHT', 'MKE', 'MMA', 'MSP',
          'MSY', 'NAS', 'NFB', 'NWY', 'OAK', 'OKC', 'OMA', 'ONT', 'ORF', 'PBI', 'PDX', 'PHL', 'PHX',
          'PIT', 'PNS', 'PUJ', 'PVD', 'PVR', 'PWM', 'RDU', 'RIC', 'RNO', 'ROC', 'RSW', 'SAN', 'SAT',
          'SDF', 'SEA', 'SFC', 'SFO', 'SJC', 'SJD', 'SJO', 'SJU', 'SLC', 'SMF', 'SNA', 'STL', 'TPA',
          'TUL', 'TUS', 'WDC']

API_URL = "https://www.southwest.com/api/air-booking/v1/air-booking/page/air/booking/shopping"
API_KEY = "l7xx944d175ea25f4b9c903a583ea82a1c4c"


def page_grab(date, depart, arrive):
    payload = {"originationAirportCode": depart,
               "destinationAirportCode": arrive,
               "departureDate": date,
               "departureTimeOfDay": "ALL_DAY",
               "returnDate": "",
               "returnTimeOfDay": "ALL_DAY",
               "adultPassengersCount": "1",
               "seniorPassengersCount": "0",
               "fareType": "USD",
               "passengerType": "ADULT",
               "tripType": "oneway",
               "reset": "true",
               "int": "HOMEQBOMAIR",
               "application": "air-booking",
               "site": "southwest"}
    headers = {'content-type': "application/json",
               'x-api-key': API_KEY,
               'dnt': '1',
               'user-agent': '',
               # Magic, but seem to always be the same
               'ee30zvqlwf-d': 'o_0',
               'ee30zvqlwf-z': 'p',
               # REPLACE THE FOLLOWING 4 LINES ACCORDING TO THE README
               'ee30zvqlwf-a': 'E7ZcHf3CtttfK7N58HZgvhB2Ran2NkskJVWiVAqeiyfavC69Qx2oqw3PrZ8nscuLrAIzIg2IUJMRe7ouynjfeuXq96P2=7QC1fY8mdXYzBqal4bP4-UaC-oV4BdiyG4e51VqqWg2gMOtcAdGwrDnCRQpow0-CFNf=hucUF0baWhXnoXn5Ifi2nSS0kXoKLnZ5GilMs=g4mM-s26kAWXYzVebCKzKNrM7qGXVi3BIdYJN2l9yBj5h96soIc2IqLAoI6ZiCHtO_Cgx4L-l9NZ6=-Mf95xxdPWU7W3gQqfO13a0xnqdzitXkIgpkbvupgwsDDa8q1jEOl=JKS-j5PoM7uXHJS-=leJ4o-alCsh2Gq0zUtV3ZHWEAWEkp9-WYCr9zxNk3bQ3479_-H5Yc=pw=apml4YRyhFGEaddRf=Q=JMdkr4pM4JvNUqkRPxKNcXrtQb5nHtW89neNLv1vR3raN3vjd4xo1AVl5sDLHaEW=JddRBfMflMklp_341CQ0Q5U9ODUjvCsJF6xQNaLs0mhl2L03kfQHyA4eVkH_SWgPcXdi-OA6APyO3a3KDmKctHvtM6q90zrV_5XM=NuApwmIX4wVfMOxevYhA=QSAc=aI07mK6ukN14GMNLNJCLQ2cUmw2_MD74oWRiV2VkBmK7ERgORMgaJa_Rc6xNzdDZA7_Sc1Jwb1NGxIIjEvSNkbK_x-7zvgXvMCZzVCnhU4uHbCQcUPJsn3HwSQ57L80wjBeMLSC8zpHrxMc8Yk8P30Aqul3Ju0hKFLm9OEIMEk2xxYIH=tUtK3xbVoLxyA2QuOUmmJ3j_fYopug1yKYMYs4NSl22XsV1SoU7osnO5tkV5qtaOu2x7-lxCv0Ksm-Il=Wx6r-FjiBU_hz=YJqj4ElWGUJ9xnBlkWNUzms9GQL31cMjbXAge2YEWibfoUwVFA==HOevMREcFSonwhAOmyI4mCrNkoPsC2zmGWIRzm64O5EqSAPgMhVr2=KPZ-tHtm4GhYUoirhZ95Ke2aKV1VlHv9O_Z0sJ2ZEE_HCUzlpunz7=KRQUZPMkUexeAGmD6BXBONQdZhkDfViq1nZxBWvM2vt8SY7F1PVIHWsy=iBgX8tWd1CBs66eU1RDpe4S51lD_jeGDC11_GuHeDSSE_drffDKSd1tgGwUOmi8LCKbx_SpSHQrVeSt7aOJJgtHdRL55Rk81U50nJwpQgA-J70ggmuCBJr4IUrkqDSN5iUNzftSda-LH=BQS47CJiKdbvoKrxWb2O8xnWR1v3EaOdHvvodRUCKsV2sZVMOBvpAmbjUilz3=f56zfJXL1Vni4lpuwbLfL=PznowexNFz7DVcOZhrs27CJaDhSgs7VsE=H6iquvvWgqUW6i1lpVbojZqyOO-JtxliisOZANIU=gw8SWsavl=n8PW_8JzndQIwgJo36Y7ja9qHIptjW424qM2-xdDC0dJVSbB-yvYHr-uOz-wt-csL-9cisaZdpPyGeL7nB_2uyuK4bNIK5veHl8Ezk10nnpqUPgt4qSPQKfM=d26XKa2dLhW_Fm_03-t_lRLnL4pJA2c-Lh6AlrdoBOkazLgaSbihYMk53sy7oQQXUCeyEL=wGqk_4=iP6Unv=8EzVM-DAg-KQr56R3j3_HaioZIpvlIL8PtVNZu-SYRxl8dkIsHyBwwsEnA0dWa4H2A1k4WwUws16QngoSRVRya=ONhLr-Pvd1xPg51GBVPaLxqkOw0MpSn-IAw0EIpdcaINlEem_NKjLBM-jWAsYcrn-2KSI1cxe-U3nCMLR3MbANgRvkWsJsra4PygXkGch5DR18sBb7YSR7P_YrDLZ3eOwZvvu8Hd7htfnKiblc-oUQhxRmFPkel_UCLr30plJO-5H7GDh6bP_cxp4lcRrajN263RJnlb9LO2uXfqYq8X9WCwC6wedJ7gBleiqj_OXj=9YM5u5b8cKMNqvE=YI_kLJ95LPRFfiCrkcWmEIeDk=Vj--gEVcP6f216502=eWgfZMh_3F=qoxknReouZEVP_3JU0m2Stskvhb6ZiZM3fbfxt39JaAzDsQ9nxoMKRiur=nIBMICE4xdl_alNPtAJXXKSZ9s8GQ0AgKgd8xjROshIpowcACNrI2gCBgj-bwZuvp4iKJGpdCbe6VcrjxnJLu4kGtl1J9PtvEccmRNtFpbsolHUV2mOmudqoXs2xGAczEV8dDr-rhoVWJB3YhqM=a=s1-d5qBgB8BbalFLXlZf8wOtCJL4h_R-cxRA1HkcrhiCbCoqzWqF8fl4ASA4dV42LbOpCoKfXcBd-dCpXEAvfX_qJR30Vaouu7SXc_L5qvbxHBB6HUcU4relf8hdSt3dDiph8G75KazijoRvyctWyOdlgHYsiMyvdoJHZoifLAvun_mQCICqvSNI=1gMb40fjcakZ9dAysOuXX1thxRrjJOgMFDc9EA5mLFWw0vNWpYeko1zsqFr6tjU4mi1HRoZ_dEwZDEz289X7YKtKuXDmWiP9SjYFocL9Ax9DORVAR554amg5w07wI3aRLFmHNfuy0EKWqGk9u-dvoGDo8sdVvV2=fvRLrk_7J2xN196PpzG01j1ZInmMgKkO6RCzkp-CEAZbBskWnmw=wIKQ-Dpp8AGkmm=b47l_-3LqoAvlKEAs5o7=Hyj0xXFb0UhWaG0-kCZ4c6BJ70Fg2aHo1RDC6ZBrskfogHW-OjqtoW=536NZjy-zJ3qj3DBhWYDYy4tcU8wDsGXFvWf17MfaIK74em7kZ3do58sFCbhdnLHMMaaypimUJB=CvqVRhCigJ6wLHOtvHVu2bbftzPsR4nc_jebcySDSr9Wm=GCLdRiktisFvJEqsblCQJGi23VjjWej0__5NpjEatXlozFtRDsgUCkK=ZkXIVmb0QDQK61XmkdO6L7pjuagwCH05lS10Bq58XJMjzE9dl_Ao64faA1lwLCiPkW1BaFqAoFlJx-5_4bvh4Fi-SFxp6JZ=7rKj8rCSV=EdJMq0KMUtlbGkzEytRkuPzd4KaJnUXCKFhEfPV65Rq3ikob8n3StOwrCF5Ka_vZPPsUQ0dNwsIiLWJuqFQ6QLha0tKgu7RgYffqZ5DdMwDOqDV4iUppuC9E_B2LPoeMRKcyuJij7SHE31aDcld4ncuWU61zGG5RUkXcFhyWHUURIB=d1HALeMfd9Naf9_U17bqY6utsQ6bMu4VzRpBglhwS2OIdcdl1Y5zecek_mir-rWYX6J0wEiShmKLgLARyX_9NC=_ibNN1SaWin89L0clzw=FutdE4NUOEFdM3waoMeQZQZIJOuu_FAIdyFOuKOXHLPg9qRGtMkrYYCEXcFRNOnGDiq-f0UD6q7xkE5',
               'ee30zvqlwf-b': '-n8teit',
               'ee30zvqlwf-c': 'AwTLNZlwAQAAlYy-zAU_rGfpJBJbZnnRNq2--pjg2rtSBtREZ8jPA3QwJg4NAUZ__oOuchShwH8AAEB3AAAAAA==',
               'ee30zvqlwf-f': 'A7UDOJlwAQAAcDYk2QAtF4CrwmYerinjU4nfURRbWpWbK4VbpNef-yawb65sAWiyD4auctuUwH8AAOfvAAAAAA==',
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

        option['flight_num'] = "/".join(flight["flightNumbers"])
        option['depart_date'] = date_pattern.match(flight['departureDateTime']).group(1)
        option['route'] = [flight['originationAirportCode']]
        for stop in flight['stopsDetails']:
            option['route'].append(stop['destinationAirportCode'])
        option['depart_time'] = date_pattern.match(flight['departureDateTime']).group(2)
        option['arrive_time'] = date_pattern.match(flight['arrivalDateTime']).group(2)
        option['num_stops'] = len(flight['stopsDetails']) - 1
        hours = flight['totalDuration'] / 60
        minutes = flight['totalDuration'] % 60
        option['duration'] = "%02i:%02i" % (hours, minutes)

        parsed.append(option)

    return parsed


def pretty_print_flights(flights, sort, lowest_fare, max_stops, reverse, verbose):
    keys = ["flight_num", "depart_date", "depart_time", "arrive_time", "fares", "route",
            "num_stops", "duration"]

    headers = []
    for key in keys:
        headers.append(key.replace("_", "\n"))

    flight_list = []
    for flight in flights:
        if max_stops is not None and flight["num_stops"] > max_stops:
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
        flight_list.sort(key=lambda item: tuple(item[keys.index(col)] for col in sort),
                         reverse=reverse)
    print tabulate.tabulate(flight_list, headers=headers)


parser = argparse.ArgumentParser()
parser.add_argument('-a', '--arrival-cities', action='store', nargs="+", required=True)
parser.add_argument('-d', '--departure-cities', action='store', nargs="+", required=True)
parser.add_argument('-t', '--dates', action='store', nargs="+", required=True, help="")
parser.add_argument('-s', '--sort', action='store', nargs="+", choices=["flight_num", "depart_time",
                    "depart_date", "arrive_time", "fares", "num_stops", "duration"],
                    help="Choose which column(s) you want to sort results by.")
parser.add_argument('-r', '--reverse', action='store_true', help="Reverse sort order for key of " +
                    "choice. If more than one key is given, all are reversed.", default=False)
parser.add_argument('-l', '--show-only-lowest-fare', action='store_true', help="Only shows the " +
                    "lowest fare for each route. (Usually a 'Wanna Get Away?' fare, but could be " +
                    "a different type.)")
parser.add_argument('-m', '--max-stops', type=int,
                    help="Filter for flights with this many stops or less.")
parser.add_argument('-e', '--export-file', type=str, help="Save results to a file. Useful if you " +
                    "want to sort and filter the same results different ways without re-making " +
                    "the server requests.")
parser.add_argument('-i', '--import-file', type=str,
                    help="Load results from a file create with --export.")
parser.add_argument('-v', '--verbose', action='store_true', help="Display verbose info about " +
                    "stops. This is usually only helpful to distinguish between stops where " +
                    "you change planes and stops where you don't have to get off the plane.")

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
