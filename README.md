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
* Python modules from pip or another source:
    * tabulate (0.7.7+)
    * selenium (3.7.0+)
* chromedriver (installed somewhere in $PATH) + dependencies
* Google Chrome

Only tested on Linux, but there's no reason it shouldn't work on OS X or Windows (if you can manage to install the Python requirements on Windows)

### Setting up and using the script on Linux
```
git clone https://github.com/redfern314/southwest-search.git
cd southwest-search
sudo pip install tabulate selenium
wget https://chromedriver.storage.googleapis.com/2.42/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/bin
# if this fails, install the packages that it suggests and repeat
chromedriver --version
python southwest.py -a ARRIVAL_CITIES -d DEPARTURE_CITIES -t DATES
```

### Example Query
```
$ python southwest.py -d SFO -a BOS -t 11/1
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