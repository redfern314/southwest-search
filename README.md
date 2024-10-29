southwest-search
================

Author: Derek Redfern

License: MIT

## Project Status - ARCHIVED
The main complaints I had when I originally wrote this tool have since been resolved:
* Southwest's main site now natively supports multiple origin/destination airports
* Southwest flights are [now available](https://www.travelandleisure.com/southwest-airlines-kayak-flights-can-be-booked-8690854) on major aggregators (Google Flights, Kayak)

and as noted in the Issues tab, this tool breaks frequently based on SW's website API changes. It's not worth it to me to continue maintaining this tool when flight aggregators have all the same functionality now.

Feel free to fork this repository if it still fits any of your needs!

## READ THIS FIRST
This script is currently mostly-broken due to some additions by SW to their API. Until it can be reverse-engineered, you'll need to do some manual steps for this to work. Screenshot to guide you is below.
1. Open up your web browser's network console (F12 -> Network in chrome)
2. Go to SW's website and make a legitimate search
3. Look for the request that was made to https://www.southwest.com/api/air-booking/v1/air-booking/page/air/booking/shopping
4. Look at the headers attached to that request. Copy and paste the ones that start with `ee30zvqlwf` (there should be 6 of them) into southwest.py at line 45. `ee30zvqlwf-d` and `ee30zvqlwf-z` likely don't need to be changed.
5. You should be able to run this script for X days after following the above steps. I'm assuming the headers will eventually expire and you'll need to regenerate them, but I don't know what X is.

![Header inspection](headers.png)

## Description
This script is a rudimentary search engine for Southwest Airlines flights. I created it because I love flying Southwest SO MUCH, but the search functionality on their website is incredibly painful when you have flexible airports or flexible dates. Flying anywhere with more than 1 or 2 variables is a nightmare - you have to open multiple browser windows to southwest.com for each possible combination.

Give southwest.py a list of airports you're able to fly out of and into, a list of dates you can fly, and what you want to optimize for (cost, time, number of stops). It'll return all possible flights sorted by your chosen criteria! Maybe you want to fly from any of the 3 SF-area airports to any of the 3 NYC-area airports anytime during the week of Thanksgiving, for example. And you want to do it cheaply. You can search for all of those parameters and get the results compiled into one list.

### Mission: Don't Anger Southwest
My goal here is to make it easier for you (and me) to fly Southwest without angering the Southwest Powers-That-Be. Southwest has previously taken down tools in this vein to protect their business model, which I respect and am trying not to disrupt. To that end:

* I will not host this to be run interactively on the web, now or at any point in the future - you must download and run it yourself.
* Be mindful that each variable you add increases the number of pages the script has to scrape on southwest.com. 3 departure airports, 3 arrival airports, and 3 dates is already a whopping 27 pages!
* The script is rate-limited (1 request every 2 seconds) to reduce the stress on the servers, so large queries may take a while to complete. Run it in the background and go do something else for a bit.

### Website updates
Any updates to the format of Southwest's API may cause very strange errors. Inputs are also not completely sanitized and may cause similar errors. If this is the case, open a Github issue and I'll try to bring it back to working order.

### Contributing
Contributions are always welcome and appreciated. I try to stick to PEP8 where I can, with max line length of 100. If you make a change, take out a PR and include testing transcripts and I'll try to merge it in ASAP.

## Installation and Usage
### Requirements
You must have, at a minimum:

* Python 2.7
* Python modules from pip or another source:
    * tabulate (0.7.7+)
    * requests

Only tested on Linux, but there's no reason it shouldn't work on OS X or Windows (if you can manage to install the Python requirements on Windows)

### Upgrade Note
The date format for the command line has changed as of September 16, 2018. Previously the date format for the command line was MM/DD/YYYY. The command line is now looking for dates in YYYY-MM-DD format.

### Setting up and using the script on Linux
```
git clone https://github.com/redfern314/southwest-search.git
cd southwest-search
sudo pip install requests tabulate
python southwest.py -a ARRIVAL_CITIES -d DEPARTURE_CITIES -t DATES
```

### Example Query
```
$ python southwest.py -d SFO -a LGA -t 2018-12-02 -s fares
Processed 1/1
flight     date        depart    arrive    fares                              route                               stops  duration
---------  ----------  --------  --------  ---------------------------------  --------------------------------  -------  ----------
4158/3971  2018-12-02  06:00     18:50     [u'139.80', u'586.58', u'614.58']  [u'SFO', u'DAL', u'LGA']                1  9:50
4158/4604  2018-12-02  06:00     16:55     [u'161.80', u'586.58', u'614.58']  [u'SFO', u'DAL', u'LGA']                1  7:55
4026/4503  2018-12-02  11:40     23:05     [u'196.80', u'586.58', u'614.58']  [u'SFO', u'STL', u'LGA']                1  8:25
2803/4491  2018-12-02  12:55     23:25     [u'323.80', u'586.58', u'614.58']  [u'SFO', u'DEN', u'LGA']                1  7:30
4324/3625  2018-12-02  09:15     22:25     [u'327.90', u'590.68', u'618.68']  [u'SFO', u'SAN', u'DAL', u'LGA']        2  10:10
```
