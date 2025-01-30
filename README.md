# WG Gesucht Tool
Finding a new appartment can be difficult some times and it is important to be always alert to find the new adds. That's why I developed a Shared Flat Web Searcher for the Website [WG-Gesucht](https://www.wg-gesucht.de/en/), which is the most known tool for finding accommodation in Germany.

## How it works
- First of all, it is necessary to set the requirements to filter the search. In [objects.py](https://github.com/juan-alvarez99/wg-gesucht-tool/blob/main/modules/objects.py) there is a dictionary with all the implemented filters for my search such as the earliest date of move, my age and my gender. 
- Using [Selenium](https://selenium-python.readthedocs.io) the search is run from the website of WG-Gesucht and the filters are applied.
- Using [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) to scrap the html code parsing the data from each ad: rent prize, size of the room...
- In order to analyze the data to estimate the cost of a room in the searched city, the results of the search are sync with Google Sheet using [Sheety](https://sheety.co/docs) to generate an API endpoint to a specific sheet. There I can play some statistics!
- If during the search a new ad is found, the app is going to send me an email with a link to the WG ad


## How to use it
1. Clone the project and create the virtual environment from the requirements.txt file
2. Create a copy of the file .env.local called .env
   
