southwest-search
================

Author: Derek Redfern

License: MIT

## Description
This script is a rudimentary search engine for Southwest Airlines flights. I created it because I love flying Southwest SO MUCH, but the search functionality on their website is incredibly painful when you have flexible airports or flexible dates. Flying anywhere with more than 1 or 2 variables is a nightmare - you have to open multiple browser windows to southwest.com for each possible combination.

Give southwest.py a list of airports you're able to fly out of and into, a list of dates you can fly, and what you want to optimize for (cost, time, number of stops). It'll return all possible flights sorted by your chosen criteria! Maybe you want to fly from any of the 3 SF-area airports to any of the 3 NYC-area airports anytime during the week of Thanksgiving, for example. And you want to do it cheaply. You can search for all of those parameters and get the results compiled into one list.

### Mission: Don't Anger Southwest
My goal here is to make it easier for you (and me) to fly Southwest without angering the Southwest Powers-That-Be. Southwest has previously taken down tools in this vein to protect their business model, which I respect and am trying not to disrupt. To that end:

* I will not host this to be run interactively on the web, now or at any point in the future - you must download and run it yourself.
* Be reasonable with the number of requests that you make to the Southwest servers.
* Be mindful that each variable you add increases the number of pages the script has to scrape on southwest.com. 3 departure airports, 3 arrival airports, and 3 dates is already a whopping 27 pages!
* The script is rate-limited (1 request every 2 seconds) to reduce the stress on the servers, so large queries may take a while to complete. Run it in the background and go do something else for a bit.

### Website updates
One thing to note is that this script relies heavily on hard-coded attributes of Southwest's website. Any updates to the site's format may cause very strange errors. If this is the case, open a Github issue and I'll try to bring it back to working order.

### Contributing
Contributions are always welcome and appreciated. I try to stick to PEP8 where I can, with max line length of 110. If you make a change, take out a PR and include testing transcripts and I'll try to merge it in ASAP.

## Installation and Usage
### Requirements
You must have, at a minimum:

* Python 2.7
* The following Python modules from pip or another source (versions are the ones I've tested with, but other versions may work):
    * bs4 (0.0.1)
    * mechanize (0.2.5)
    * tabulate (0.7.5)

Only tested on Linux, but there's no reason it shouldn't work on OS X or Windows (if you can manage to install the Python requirements on Windows)

### Using the script on Linux
```
git clone https://github.com/redfern314/southwest-search.git
cd southwest-search
sudo pip install bs4 mechanize tabulate
python southwest.py -a ARRIVAL_CITIES -d DEPARTURE_CITIES -t DATES
```

### Example Queries
Note: you will want to make your terminal window very wide if you add flags like `-v`
#### A simple flight from San Francisco to Boston
```
$ python southwest.py -d SFO -a BOS -t 11/1/2016
Processed 1/1
flight_num    depart            arrive            fares            route                               num_stops  flight_time
------------  ----------------  ----------------  ---------------  --------------------------------  -----------  -------------
287/2304      2016/11/01 11:00  2016/11/02 00:05  [157, 662, 690]  [u'SFO', u'DEN', u'BOS']                    1  10:05
2899/1415     2016/11/01 06:10  2016/11/01 16:40  [157, 662, 690]  [u'SFO', u'DEN', u'BOS']                    1  07:30
2661/484      2016/11/01 14:05  2016/11/02 01:05  [157, 662, 690]  [u'SFO', u'MDW', u'BOS']                    1  08:00
995/5444      2016/11/01 06:25  2016/11/01 18:50  [161, 666, 694]  [u'SFO', u'MDW', u'BWI', u'BOS']            2  09:25
995/2288      2016/11/01 06:25  2016/11/01 17:00  [157, 662, 690]  [u'SFO', u'MDW', u'BOS']                    1  07:35
806/678       2016/11/01 08:20  2016/11/01 20:35  [157, 662, 690]  [u'SFO', u'MDW', u'BOS']                    1  09:15
```

#### Show me details of where I'd be stopping
```
$ python southwest.py -d SFO -a BOS -t 11/1/2016 -v
Processed 1/1
flight_num    depart            arrive            fares            route                               num_stops  flight_time    stop_info
------------  ----------------  ----------------  ---------------  --------------------------------  -----------  -------------  ----------------------------
287/2304      2016/11/01 11:00  2016/11/02 00:05  [157, 662, 690]  [u'SFO', u'DEN', u'BOS']                    1  10:05          1 stop Change Planes in DEN
2899/1415     2016/11/01 06:10  2016/11/01 16:40  [157, 662, 690]  [u'SFO', u'DEN', u'BOS']                    1  07:30          1 stop Change Planes in DEN
2661/484      2016/11/01 14:05  2016/11/02 01:05  [157, 662, 690]  [u'SFO', u'MDW', u'BOS']                    1  08:00          1 stop Change Planes in MDW
995/5444      2016/11/01 06:25  2016/11/01 18:50  [161, 666, 694]  [u'SFO', u'MDW', u'BWI', u'BOS']            2  09:25          2 stops Change Planes in BWI
995/2288      2016/11/01 06:25  2016/11/01 17:00  [157, 662, 690]  [u'SFO', u'MDW', u'BOS']                    1  07:35          1 stop Change Planes in MDW
806/678       2016/11/01 08:20  2016/11/01 20:35  [157, 662, 690]  [u'SFO', u'MDW', u'BOS']                    1  09:15          1 stop Change Planes in MDW
```

#### Don't make me stop more than once!
```
$ python southwest.py -d SFO -a BOS -t 11/1/2016 -m 1
Processed 1/1
flight_num    depart            arrive            fares            route                       num_stops  flight_time
------------  ----------------  ----------------  ---------------  ------------------------  -----------  -------------
287/2304      2016/11/01 11:00  2016/11/02 00:05  [157, 662, 690]  [u'SFO', u'DEN', u'BOS']            1  10:05
2899/1415     2016/11/01 06:10  2016/11/01 16:40  [157, 662, 690]  [u'SFO', u'DEN', u'BOS']            1  07:30
2661/484      2016/11/01 14:05  2016/11/02 01:05  [157, 662, 690]  [u'SFO', u'MDW', u'BOS']            1  08:00
995/2288      2016/11/01 06:25  2016/11/01 17:00  [157, 662, 690]  [u'SFO', u'MDW', u'BOS']            1  07:35
806/678       2016/11/01 08:20  2016/11/01 20:35  [157, 662, 690]  [u'SFO', u'MDW', u'BOS']            1  09:15
```

#### Get me there as fast as possible!
```
$ python southwest.py -d SFO -a BOS -t 11/1/2016 -s flight_time
Processed 1/1
flight_num    depart            arrive            fares            route                               num_stops  flight_time
------------  ----------------  ----------------  ---------------  --------------------------------  -----------  -------------
2899/1415     2016/11/01 06:10  2016/11/01 16:40  [157, 662, 690]  [u'SFO', u'DEN', u'BOS']                    1  07:30
995/2288      2016/11/01 06:25  2016/11/01 17:00  [157, 662, 690]  [u'SFO', u'MDW', u'BOS']                    1  07:35
2661/484      2016/11/01 14:05  2016/11/02 01:05  [157, 662, 690]  [u'SFO', u'MDW', u'BOS']                    1  08:00
806/678       2016/11/01 08:20  2016/11/01 20:35  [157, 662, 690]  [u'SFO', u'MDW', u'BOS']                    1  09:15
995/5444      2016/11/01 06:25  2016/11/01 18:50  [161, 666, 694]  [u'SFO', u'MDW', u'BWI', u'BOS']            2  09:25
287/2304      2016/11/01 11:00  2016/11/02 00:05  [157, 662, 690]  [u'SFO', u'DEN', u'BOS']                    1  10:05
```

#### Going to Chicago, but I can fly out of any of the 3 SF-area airports if it gets me a better price (and no business class for me)
```
$ python southwest.py -d SFO OAK SJC -a MDW -t 11/1/2016 -s fares --show-only-lowest-fare
Processed 1/3
Processed 2/3
Processed 3/3
flight_num    depart            arrive              fares  route                       num_stops  flight_time
------------  ----------------  ----------------  -------  ------------------------  -----------  -------------
995           2016/11/01 06:25  2016/11/01 12:40       64  [u'SFO', u'MDW']                    0  04:15
2661          2016/11/01 14:05  2016/11/01 20:15       64  [u'SFO', u'MDW']                    0  04:10
806           2016/11/01 08:20  2016/11/01 14:30       64  [u'SFO', u'MDW']                    0  04:10
888           2016/11/01 08:55  2016/11/01 15:00       99  [u'OAK', u'MDW']                    0  04:05
168           2016/11/01 13:40  2016/11/01 19:45       99  [u'OAK', u'MDW']                    0  04:05
2494          2016/11/01 14:35  2016/11/01 20:40       99  [u'OAK', u'MDW']                    0  04:05
2243          2016/11/01 06:40  2016/11/01 12:50       99  [u'OAK', u'MDW']                    0  04:10
2622          2016/11/01 08:40  2016/11/01 14:50       99  [u'SJC', u'MDW']                    0  04:10
186           2016/11/01 08:05  2016/11/01 15:20      128  [u'OAK', u'STL', u'MDW']            1  05:15
2023          2016/11/01 06:15  2016/11/01 14:05      128  [u'OAK', u'LAX', u'MDW']            1  05:50
3055          2016/11/01 07:00  2016/11/01 16:15      128  [u'SJC', u'SEA', u'MDW']            1  07:15
635/2486      2016/11/01 14:50  2016/11/01 22:45      132  [u'SFO', u'DEN', u'MDW']            1  05:55
2615/549      2016/11/01 08:55  2016/11/01 16:55      132  [u'SFO', u'STL', u'MDW']            1  06:00
3522/2287     2016/11/01 11:25  2016/11/01 20:10      132  [u'SFO', u'SAN', u'MDW']            1  06:45
519/2486      2016/11/01 14:40  2016/11/01 22:45      132  [u'OAK', u'DEN', u'MDW']            1  06:05
2933/678      2016/11/01 06:45  2016/11/01 16:20      132  [u'OAK', u'SLC', u'MDW']            1  07:35
401/1173      2016/11/01 16:30  2016/11/01 23:50      132  [u'OAK', u'DEN', u'MDW']            1  05:20
1885/505      2016/11/01 11:40  2016/11/01 20:10      132  [u'OAK', u'DEN', u'MDW']            1  06:30
1433/2294     2016/11/01 15:05  2016/11/01 23:15      132  [u'SJC', u'DAL', u'MDW']            1  06:10
2867          2016/11/01 07:40  2016/11/01 16:40      153  [u'OAK', u'HOU', u'MDW']            1  07:00
716           2016/11/01 12:55  2016/11/01 20:40      153  [u'OAK', u'LAX', u'MDW']            1  05:45
1987/3608     2016/11/01 08:05  2016/11/01 16:30      157  [u'SFO', u'SAN', u'MDW']            1  06:25
287/2986      2016/11/01 11:00  2016/11/01 18:55      157  [u'SFO', u'DEN', u'MDW']            1  05:55
699/1353      2016/11/01 09:20  2016/11/01 18:10      157  [u'SFO', u'LAS', u'MDW']            1  06:50
1937/716      2016/11/01 11:40  2016/11/01 20:40      157  [u'SFO', u'LAX', u'MDW']            1  07:00
2845/1430     2016/11/01 15:20  2016/11/01 23:20      157  [u'SFO', u'LAS', u'MDW']            1  06:00
2899/518      2016/11/01 06:10  2016/11/01 14:20      157  [u'SFO', u'DEN', u'MDW']            1  06:10
2606/716      2016/11/01 11:45  2016/11/01 20:40      157  [u'OAK', u'LAX', u'MDW']            1  06:55
423/1430      2016/11/01 14:25  2016/11/01 23:20      157  [u'OAK', u'LAS', u'MDW']            1  06:55
1885/2986     2016/11/01 11:40  2016/11/01 18:55      157  [u'OAK', u'DEN', u'MDW']            1  05:15
1992/1430     2016/11/01 15:30  2016/11/01 23:20      157  [u'SJC', u'LAS', u'MDW']            1  05:50
478/1974      2016/11/01 09:20  2016/11/01 17:35      157  [u'SJC', u'PHX', u'MDW']            1  06:15
2207/484      2016/11/01 13:35  2016/11/01 21:10      157  [u'SJC', u'DEN', u'MDW']            1  05:35
482/518       2016/11/01 06:30  2016/11/01 14:20      157  [u'SJC', u'DEN', u'MDW']            1  05:50
3660/1353     2016/11/01 09:35  2016/11/01 18:10      157  [u'SJC', u'LAS', u'MDW']            1  06:35
1895/140      2016/11/01 16:25  2016/11/02 00:25      157  [u'SJC', u'LAX', u'MDW']            1  06:00
1849          2016/11/01 11:40  2016/11/01 19:30      163  [u'SJC', u'LAX', u'MDW']            1  05:50
3121/2151     2016/11/01 06:00  2016/11/01 15:15      167  [u'SFO', u'LAX', u'MDW']            1  07:15
588/1223      2016/11/01 14:00  2016/11/01 21:50      167  [u'SFO', u'LAS', u'MDW']            1  05:50
2562/1849     2016/11/01 10:25  2016/11/01 19:30      167  [u'SFO', u'LAX', u'MDW']            1  07:05
578/2125      2016/11/01 11:55  2016/11/01 20:20      167  [u'SFO', u'PHX', u'MDW']            1  06:25
2369/2177     2016/11/01 07:45  2016/11/01 16:35      167  [u'OAK', u'PHX', u'MDW']            1  06:50
494/2177      2016/11/01 07:40  2016/11/01 16:35      167  [u'SJC', u'PHX', u'MDW']            1  06:55
2747/2151     2016/11/01 06:30  2016/11/01 15:15      167  [u'SJC', u'LAX', u'MDW']            1  06:45
2461/1849     2016/11/01 10:30  2016/11/01 19:30      167  [u'SJC', u'LAX', u'MDW']            1  07:00
538/1363      2016/11/01 16:10  2016/11/01 23:55      167  [u'SJC', u'PHX', u'MDW']            1  05:45
331/1223      2016/11/01 13:05  2016/11/01 21:50      167  [u'SJC', u'LAS', u'MDW']            1  06:45
6566          2016/11/01 12:55  2016/11/01 20:35      228  [u'OAK', u'LAS', u'MDW']            1  05:40
2610/199      2016/11/01 06:15  2016/11/01 14:50      232  [u'SFO', u'SNA', u'MDW']            1  06:35
470/6566      2016/11/01 12:25  2016/11/01 20:35      232  [u'SFO', u'LAS', u'MDW']            1  06:10
535/1353      2016/11/01 09:35  2016/11/01 18:10      232  [u'OAK', u'LAS', u'MDW']            1  06:35
1465/354      2016/11/01 12:10  2016/11/01 19:55      232  [u'SJC', u'LAS', u'MDW']            1  05:45
2551/2232     2016/11/01 08:45  2016/11/01 16:50      232  [u'SJC', u'LAS', u'MDW']            1  06:05
2697/199      2016/11/01 06:35  2016/11/01 14:50      232  [u'SJC', u'SNA', u'MDW']            1  06:15
```

#### I know my airports and dates, but want to play around with sorting... export the data so it only has to be grabbed once
```
$ python southwest.py -d SFO OAK SJC -a MDW -t 11/1/2016 -s fares --show-only-lowest-fare -e chicago.json
Processed 1/3
Processed 2/3
Processed 3/3
flight_num    depart            arrive              fares  route                       num_stops  flight_time
------------  ----------------  ----------------  -------  ------------------------  -----------  -------------
995           2016/11/01 06:25  2016/11/01 12:40       64  [u'SFO', u'MDW']                    0  04:15
2661          2016/11/01 14:05  2016/11/01 20:15       64  [u'SFO', u'MDW']                    0  04:10
806           2016/11/01 08:20  2016/11/01 14:30       64  [u'SFO', u'MDW']                    0  04:10
888           2016/11/01 08:55  2016/11/01 15:00       99  [u'OAK', u'MDW']                    0  04:05
168           2016/11/01 13:40  2016/11/01 19:45       99  [u'OAK', u'MDW']                    0  04:05
2494          2016/11/01 14:35  2016/11/01 20:40       99  [u'OAK', u'MDW']                    0  04:05
2243          2016/11/01 06:40  2016/11/01 12:50       99  [u'OAK', u'MDW']                    0  04:10
2622          2016/11/01 08:40  2016/11/01 14:50       99  [u'SJC', u'MDW']                    0  04:10
186           2016/11/01 08:05  2016/11/01 15:20      128  [u'OAK', u'STL', u'MDW']            1  05:15
2023          2016/11/01 06:15  2016/11/01 14:05      128  [u'OAK', u'LAX', u'MDW']            1  05:50
3055          2016/11/01 07:00  2016/11/01 16:15      128  [u'SJC', u'SEA', u'MDW']            1  07:15
635/2486      2016/11/01 14:50  2016/11/01 22:45      132  [u'SFO', u'DEN', u'MDW']            1  05:55
2615/549      2016/11/01 08:55  2016/11/01 16:55      132  [u'SFO', u'STL', u'MDW']            1  06:00
3522/2287     2016/11/01 11:25  2016/11/01 20:10      132  [u'SFO', u'SAN', u'MDW']            1  06:45
519/2486      2016/11/01 14:40  2016/11/01 22:45      132  [u'OAK', u'DEN', u'MDW']            1  06:05
2933/678      2016/11/01 06:45  2016/11/01 16:20      132  [u'OAK', u'SLC', u'MDW']            1  07:35
401/1173      2016/11/01 16:30  2016/11/01 23:50      132  [u'OAK', u'DEN', u'MDW']            1  05:20
1885/505      2016/11/01 11:40  2016/11/01 20:10      132  [u'OAK', u'DEN', u'MDW']            1  06:30
1433/2294     2016/11/01 15:05  2016/11/01 23:15      132  [u'SJC', u'DAL', u'MDW']            1  06:10
2867          2016/11/01 07:40  2016/11/01 16:40      153  [u'OAK', u'HOU', u'MDW']            1  07:00
716           2016/11/01 12:55  2016/11/01 20:40      153  [u'OAK', u'LAX', u'MDW']            1  05:45
1987/3608     2016/11/01 08:05  2016/11/01 16:30      157  [u'SFO', u'SAN', u'MDW']            1  06:25
287/2986      2016/11/01 11:00  2016/11/01 18:55      157  [u'SFO', u'DEN', u'MDW']            1  05:55
699/1353      2016/11/01 09:20  2016/11/01 18:10      157  [u'SFO', u'LAS', u'MDW']            1  06:50
1937/716      2016/11/01 11:40  2016/11/01 20:40      157  [u'SFO', u'LAX', u'MDW']            1  07:00
2845/1430     2016/11/01 15:20  2016/11/01 23:20      157  [u'SFO', u'LAS', u'MDW']            1  06:00
2899/518      2016/11/01 06:10  2016/11/01 14:20      157  [u'SFO', u'DEN', u'MDW']            1  06:10
2606/716      2016/11/01 11:45  2016/11/01 20:40      157  [u'OAK', u'LAX', u'MDW']            1  06:55
423/1430      2016/11/01 14:25  2016/11/01 23:20      157  [u'OAK', u'LAS', u'MDW']            1  06:55
1885/2986     2016/11/01 11:40  2016/11/01 18:55      157  [u'OAK', u'DEN', u'MDW']            1  05:15
1992/1430     2016/11/01 15:30  2016/11/01 23:20      157  [u'SJC', u'LAS', u'MDW']            1  05:50
478/1974      2016/11/01 09:20  2016/11/01 17:35      157  [u'SJC', u'PHX', u'MDW']            1  06:15
2207/484      2016/11/01 13:35  2016/11/01 21:10      157  [u'SJC', u'DEN', u'MDW']            1  05:35
482/518       2016/11/01 06:30  2016/11/01 14:20      157  [u'SJC', u'DEN', u'MDW']            1  05:50
3660/1353     2016/11/01 09:35  2016/11/01 18:10      157  [u'SJC', u'LAS', u'MDW']            1  06:35
1895/140      2016/11/01 16:25  2016/11/02 00:25      157  [u'SJC', u'LAX', u'MDW']            1  06:00
1849          2016/11/01 11:40  2016/11/01 19:30      163  [u'SJC', u'LAX', u'MDW']            1  05:50
3121/2151     2016/11/01 06:00  2016/11/01 15:15      167  [u'SFO', u'LAX', u'MDW']            1  07:15
588/1223      2016/11/01 14:00  2016/11/01 21:50      167  [u'SFO', u'LAS', u'MDW']            1  05:50
2562/1849     2016/11/01 10:25  2016/11/01 19:30      167  [u'SFO', u'LAX', u'MDW']            1  07:05
578/2125      2016/11/01 11:55  2016/11/01 20:20      167  [u'SFO', u'PHX', u'MDW']            1  06:25
2369/2177     2016/11/01 07:45  2016/11/01 16:35      167  [u'OAK', u'PHX', u'MDW']            1  06:50
494/2177      2016/11/01 07:40  2016/11/01 16:35      167  [u'SJC', u'PHX', u'MDW']            1  06:55
2747/2151     2016/11/01 06:30  2016/11/01 15:15      167  [u'SJC', u'LAX', u'MDW']            1  06:45
2461/1849     2016/11/01 10:30  2016/11/01 19:30      167  [u'SJC', u'LAX', u'MDW']            1  07:00
538/1363      2016/11/01 16:10  2016/11/01 23:55      167  [u'SJC', u'PHX', u'MDW']            1  05:45
331/1223      2016/11/01 13:05  2016/11/01 21:50      167  [u'SJC', u'LAS', u'MDW']            1  06:45
6566          2016/11/01 12:55  2016/11/01 20:35      228  [u'OAK', u'LAS', u'MDW']            1  05:40
2610/199      2016/11/01 06:15  2016/11/01 14:50      232  [u'SFO', u'SNA', u'MDW']            1  06:35
470/6566      2016/11/01 12:25  2016/11/01 20:35      232  [u'SFO', u'LAS', u'MDW']            1  06:10
535/1353      2016/11/01 09:35  2016/11/01 18:10      232  [u'OAK', u'LAS', u'MDW']            1  06:35
1465/354      2016/11/01 12:10  2016/11/01 19:55      232  [u'SJC', u'LAS', u'MDW']            1  05:45
2551/2232     2016/11/01 08:45  2016/11/01 16:50      232  [u'SJC', u'LAS', u'MDW']            1  06:05
2697/199      2016/11/01 06:35  2016/11/01 14:50      232  [u'SJC', u'SNA', u'MDW']            1  06:15
```

#### I realized I need to arrive as early as possible, so use the exported data to change the sort order (without making the requests again)
```
$ python southwest.py -d SFO OAK SJC -a MDW -t 11/1/2016 -s arrive --show-only-lowest-fare -i chicago.json
flight_num    depart            arrive              fares  route                       num_stops  flight_time
------------  ----------------  ----------------  -------  ------------------------  -----------  -------------
995           2016/11/01 06:25  2016/11/01 12:40       64  [u'SFO', u'MDW']                    0  04:15
2243          2016/11/01 06:40  2016/11/01 12:50       99  [u'OAK', u'MDW']                    0  04:10
2023          2016/11/01 06:15  2016/11/01 14:05      128  [u'OAK', u'LAX', u'MDW']            1  05:50
2899/518      2016/11/01 06:10  2016/11/01 14:20      157  [u'SFO', u'DEN', u'MDW']            1  06:10
482/518       2016/11/01 06:30  2016/11/01 14:20      157  [u'SJC', u'DEN', u'MDW']            1  05:50
806           2016/11/01 08:20  2016/11/01 14:30       64  [u'SFO', u'MDW']                    0  04:10
2610/199      2016/11/01 06:15  2016/11/01 14:50      232  [u'SFO', u'SNA', u'MDW']            1  06:35
2622          2016/11/01 08:40  2016/11/01 14:50       99  [u'SJC', u'MDW']                    0  04:10
2697/199      2016/11/01 06:35  2016/11/01 14:50      232  [u'SJC', u'SNA', u'MDW']            1  06:15
888           2016/11/01 08:55  2016/11/01 15:00       99  [u'OAK', u'MDW']                    0  04:05
3121/2151     2016/11/01 06:00  2016/11/01 15:15      167  [u'SFO', u'LAX', u'MDW']            1  07:15
2747/2151     2016/11/01 06:30  2016/11/01 15:15      167  [u'SJC', u'LAX', u'MDW']            1  06:45
186           2016/11/01 08:05  2016/11/01 15:20      128  [u'OAK', u'STL', u'MDW']            1  05:15
3055          2016/11/01 07:00  2016/11/01 16:15      128  [u'SJC', u'SEA', u'MDW']            1  07:15
2933/678      2016/11/01 06:45  2016/11/01 16:20      132  [u'OAK', u'SLC', u'MDW']            1  07:35
1987/3608     2016/11/01 08:05  2016/11/01 16:30      157  [u'SFO', u'SAN', u'MDW']            1  06:25
2369/2177     2016/11/01 07:45  2016/11/01 16:35      167  [u'OAK', u'PHX', u'MDW']            1  06:50
494/2177      2016/11/01 07:40  2016/11/01 16:35      167  [u'SJC', u'PHX', u'MDW']            1  06:55
2867          2016/11/01 07:40  2016/11/01 16:40      153  [u'OAK', u'HOU', u'MDW']            1  07:00
2551/2232     2016/11/01 08:45  2016/11/01 16:50      232  [u'SJC', u'LAS', u'MDW']            1  06:05
2615/549      2016/11/01 08:55  2016/11/01 16:55      132  [u'SFO', u'STL', u'MDW']            1  06:00
478/1974      2016/11/01 09:20  2016/11/01 17:35      157  [u'SJC', u'PHX', u'MDW']            1  06:15
699/1353      2016/11/01 09:20  2016/11/01 18:10      157  [u'SFO', u'LAS', u'MDW']            1  06:50
535/1353      2016/11/01 09:35  2016/11/01 18:10      232  [u'OAK', u'LAS', u'MDW']            1  06:35
3660/1353     2016/11/01 09:35  2016/11/01 18:10      157  [u'SJC', u'LAS', u'MDW']            1  06:35
287/2986      2016/11/01 11:00  2016/11/01 18:55      157  [u'SFO', u'DEN', u'MDW']            1  05:55
1885/2986     2016/11/01 11:40  2016/11/01 18:55      157  [u'OAK', u'DEN', u'MDW']            1  05:15
2562/1849     2016/11/01 10:25  2016/11/01 19:30      167  [u'SFO', u'LAX', u'MDW']            1  07:05
1849          2016/11/01 11:40  2016/11/01 19:30      163  [u'SJC', u'LAX', u'MDW']            1  05:50
2461/1849     2016/11/01 10:30  2016/11/01 19:30      167  [u'SJC', u'LAX', u'MDW']            1  07:00
168           2016/11/01 13:40  2016/11/01 19:45       99  [u'OAK', u'MDW']                    0  04:05
1465/354      2016/11/01 12:10  2016/11/01 19:55      232  [u'SJC', u'LAS', u'MDW']            1  05:45
3522/2287     2016/11/01 11:25  2016/11/01 20:10      132  [u'SFO', u'SAN', u'MDW']            1  06:45
1885/505      2016/11/01 11:40  2016/11/01 20:10      132  [u'OAK', u'DEN', u'MDW']            1  06:30
2661          2016/11/01 14:05  2016/11/01 20:15       64  [u'SFO', u'MDW']                    0  04:10
578/2125      2016/11/01 11:55  2016/11/01 20:20      167  [u'SFO', u'PHX', u'MDW']            1  06:25
470/6566      2016/11/01 12:25  2016/11/01 20:35      232  [u'SFO', u'LAS', u'MDW']            1  06:10
6566          2016/11/01 12:55  2016/11/01 20:35      228  [u'OAK', u'LAS', u'MDW']            1  05:40
1937/716      2016/11/01 11:40  2016/11/01 20:40      157  [u'SFO', u'LAX', u'MDW']            1  07:00
716           2016/11/01 12:55  2016/11/01 20:40      153  [u'OAK', u'LAX', u'MDW']            1  05:45
2606/716      2016/11/01 11:45  2016/11/01 20:40      157  [u'OAK', u'LAX', u'MDW']            1  06:55
2494          2016/11/01 14:35  2016/11/01 20:40       99  [u'OAK', u'MDW']                    0  04:05
2207/484      2016/11/01 13:35  2016/11/01 21:10      157  [u'SJC', u'DEN', u'MDW']            1  05:35
588/1223      2016/11/01 14:00  2016/11/01 21:50      167  [u'SFO', u'LAS', u'MDW']            1  05:50
331/1223      2016/11/01 13:05  2016/11/01 21:50      167  [u'SJC', u'LAS', u'MDW']            1  06:45
635/2486      2016/11/01 14:50  2016/11/01 22:45      132  [u'SFO', u'DEN', u'MDW']            1  05:55
519/2486      2016/11/01 14:40  2016/11/01 22:45      132  [u'OAK', u'DEN', u'MDW']            1  06:05
1433/2294     2016/11/01 15:05  2016/11/01 23:15      132  [u'SJC', u'DAL', u'MDW']            1  06:10
2845/1430     2016/11/01 15:20  2016/11/01 23:20      157  [u'SFO', u'LAS', u'MDW']            1  06:00
423/1430      2016/11/01 14:25  2016/11/01 23:20      157  [u'OAK', u'LAS', u'MDW']            1  06:55
1992/1430     2016/11/01 15:30  2016/11/01 23:20      157  [u'SJC', u'LAS', u'MDW']            1  05:50
401/1173      2016/11/01 16:30  2016/11/01 23:50      132  [u'OAK', u'DEN', u'MDW']            1  05:20
538/1363      2016/11/01 16:10  2016/11/01 23:55      167  [u'SJC', u'PHX', u'MDW']            1  05:45
1895/140      2016/11/01 16:25  2016/11/02 00:25      157  [u'SJC', u'LAX', u'MDW']            1  06:00

```

#### I'm super flexible with dates and airports - is there a flight for Thanksgiving that won't cost an arm and a leg?
(Answer: not unless you're willing to fly day-of)
```
$ python southwest.py -d SFO OAK SJC -a BOS -t 11/22/2016 11/23/2016 11/24/2016 -s fares
Processed 1/9
Processed 2/9
Processed 3/9
Processed 4/9
Processed 5/9
Processed 6/9
Processed 7/9
Processed 8/9
Processed 9/9
flight_num    depart            arrive            fares            route                               num_stops  flight_time
------------  ----------------  ----------------  ---------------  --------------------------------  -----------  -------------
4480/5028     2016/11/24 05:40  2016/11/24 15:40  [192, 662, 690]  [u'SFO', u'DEN', u'BOS']                    1  07:00
2276/2919     2016/11/24 06:30  2016/11/24 16:40  [222, 580, 608]  [u'SJC', u'BWI', u'BOS']                    1  07:10
4204/5028     2016/11/24 05:40  2016/11/24 15:40  [231, 587, 615]  [u'OAK', u'DEN', u'BOS']                    1  07:00
1900/941      2016/11/24 06:40  2016/11/24 17:00  [252, 580, 608]  [u'SJC', u'DAL', u'BOS']                    1  07:20
2966/4471     2016/11/24 06:10  2016/11/24 16:45  [262, 662, 690]  [u'SFO', u'MDW', u'BOS']                    1  07:35
2309/4471     2016/11/24 06:00  2016/11/24 16:45  [263, 587, 615]  [u'OAK', u'MDW', u'BOS']                    1  07:45
4592          2016/11/23 13:35  2016/11/23 23:30  [313, 677, 705]  [u'SFO', u'STL', u'BOS']                    1  06:55
6578/4199     2016/11/23 14:40  2016/11/24 01:55  [317, 682, 710]  [u'SFO', u'MDW', u'BOS']                    1  08:15
3269/4925     2016/11/22 05:45  2016/11/22 17:10  [335, 587, 615]  [u'OAK', u'MDW', u'BOS']                    1  08:25
4231/2087     2016/11/24 07:55  2016/11/24 21:10  [335, 587, 615]  [u'OAK', u'HOU', u'BOS']                    1  10:15
4416/6381     2016/11/22 11:45  2016/11/22 23:00  [344, 662, 690]  [u'SFO', u'MDW', u'BOS']                    1  08:15
3571/4925     2016/11/22 06:00  2016/11/22 17:10  [344, 662, 690]  [u'SFO', u'MDW', u'BOS']                    1  08:10
6578/4199     2016/11/22 14:40  2016/11/23 01:55  [344, 662, 690]  [u'SFO', u'MDW', u'BOS']                    1  08:15
4192/5818     2016/11/23 13:45  2016/11/24 00:25  [345, 607, 635]  [u'OAK', u'MDW', u'BOS']                    1  07:40
3269/4925     2016/11/23 05:45  2016/11/23 17:10  [345, 607, 635]  [u'OAK', u'MDW', u'BOS']                    1  08:25
4416/6381     2016/11/23 11:45  2016/11/23 23:00  [354, 682, 710]  [u'SFO', u'MDW', u'BOS']                    1  08:15
3571/4925     2016/11/23 06:00  2016/11/23 17:10  [354, 682, 710]  [u'SFO', u'MDW', u'BOS']                    1  08:10
4192/5818     2016/11/22 13:45  2016/11/23 00:25  [385, 587, 615]  [u'OAK', u'MDW', u'BOS']                    1  07:40
2035/4199     2016/11/22 15:20  2016/11/23 01:55  [385, 587, 615]  [u'OAK', u'MDW', u'BOS']                    1  07:35
2035/4199     2016/11/23 15:20  2016/11/24 01:55  [395, 607, 635]  [u'OAK', u'MDW', u'BOS']                    1  07:35
6074/4199     2016/11/22 15:45  2016/11/23 01:55  [397, 580, 608]  [u'SJC', u'MDW', u'BOS']                    1  07:10
5580/2253     2016/11/22 10:35  2016/11/22 22:45  [401, 584, 612]  [u'SJC', u'SAN', u'HOU', u'BOS']            2  09:10
6257/3592     2016/11/23 14:35  2016/11/24 01:10  [407, 600, 628]  [u'SJC', u'DEN', u'BOS']                    1  07:35
6074/4199     2016/11/23 15:45  2016/11/24 01:55  [407, 600, 628]  [u'SJC', u'MDW', u'BOS']                    1  07:10
3613/3980     2016/11/23 07:55  2016/11/23 18:20  [407, 600, 628]  [u'SJC', u'BWI', u'BOS']                    1  07:25
3742/4645     2016/11/22 07:50  2016/11/22 18:30  [407, 662, 690]  [u'SFO', u'DEN', u'BOS']                    1  07:40
3742/4645     2016/11/23 07:50  2016/11/23 18:30  [417, 682, 710]  [u'SFO', u'DEN', u'BOS']                    1  07:40
6257/3592     2016/11/22 14:35  2016/11/23 01:10  [580, 608]       [u'SJC', u'DEN', u'BOS']                    1  07:35
3613/3980     2016/11/22 07:55  2016/11/22 18:20  [580, 608]       [u'SJC', u'BWI', u'BOS']                    1  07:25
5309/3634     2016/11/22 05:30  2016/11/22 15:30  [587, 615]       [u'OAK', u'DEN', u'BOS']                    1  07:00
4933/6237     2016/11/22 07:10  2016/11/22 17:25  [587, 615]       [u'OAK', u'BWI', u'BOS']                    1  07:15
2825/4535     2016/11/22 07:35  2016/11/22 18:05  [587, 615]       [u'OAK', u'BNA', u'BOS']                    1  07:30
2099/3562     2016/11/22 08:30  2016/11/22 20:55  [587, 615]       [u'OAK', u'MDW', u'BOS']                    1  09:25
4933/3980     2016/11/22 07:10  2016/11/22 18:20  [587, 615]       [u'OAK', u'BWI', u'BOS']                    1  08:10
4240/4592     2016/11/22 13:45  2016/11/22 23:30  [587, 615]       [u'OAK', u'STL', u'BOS']                    1  06:45
5135/5914     2016/11/22 14:10  2016/11/23 00:40  [587, 615]       [u'OAK', u'BWI', u'BOS']                    1  07:30
3816/4645     2016/11/22 08:25  2016/11/22 18:30  [587, 615]       [u'OAK', u'DEN', u'BOS']                    1  07:05
3809/2807     2016/11/22 09:45  2016/11/22 21:45  [591, 619]       [u'OAK', u'PHX', u'AUS', u'BOS']            2  09:00
5580/2253     2016/11/23 10:35  2016/11/23 22:45  [604, 632]       [u'SJC', u'SAN', u'HOU', u'BOS']            2  09:10
5309/3634     2016/11/23 05:30  2016/11/23 15:30  [607, 635]       [u'OAK', u'DEN', u'BOS']                    1  07:00
4933/6237     2016/11/23 07:10  2016/11/23 17:25  [607, 635]       [u'OAK', u'BWI', u'BOS']                    1  07:15
2825/4535     2016/11/23 07:35  2016/11/23 18:05  [607, 635]       [u'OAK', u'BNA', u'BOS']                    1  07:30
2099/3562     2016/11/23 08:30  2016/11/23 20:55  [607, 635]       [u'OAK', u'MDW', u'BOS']                    1  09:25
4933/3980     2016/11/23 07:10  2016/11/23 18:20  [607, 635]       [u'OAK', u'BWI', u'BOS']                    1  08:10
4240/4592     2016/11/23 13:45  2016/11/23 23:30  [607, 635]       [u'OAK', u'STL', u'BOS']                    1  06:45
5135/5914     2016/11/23 14:10  2016/11/24 00:40  [607, 635]       [u'OAK', u'BWI', u'BOS']                    1  07:30
3816/4645     2016/11/23 08:25  2016/11/23 18:30  [607, 635]       [u'OAK', u'DEN', u'BOS']                    1  07:05
3809/2807     2016/11/23 09:45  2016/11/23 21:45  [611, 639]       [u'OAK', u'PHX', u'AUS', u'BOS']            2  09:00
4592          2016/11/22 13:35  2016/11/22 23:30  [657, 685]       [u'SFO', u'STL', u'BOS']                    1  06:55
4277/3634     2016/11/22 05:20  2016/11/22 15:30  [662, 690]       [u'SFO', u'DEN', u'BOS']                    1  07:10
4277/3634     2016/11/23 05:20  2016/11/23 15:30  [682, 710]       [u'SFO', u'DEN', u'BOS']                    1  07:10
```
