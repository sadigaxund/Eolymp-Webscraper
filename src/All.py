
# Import Required Modules
from logging import WARNING
from bs4 import BeautifulSoup
from header import LogUtil as Logger
import requests
import warnings
warnings.filterwarnings("ignore")

import os
p = os.path.abspath('..')

dataPath = str(p) + "\data"
logPath =  dataPath + "\info.log"


logger = Logger(logPath)
out_tsvFile = dataPath + "/all_raw.tsv"
delim = '\t'
header = ["ID", "Problem"]
firstPage = 318
lastPage = 325

# Log helper method
def log(msg, type):
    logger.print(msg, type)
    logger.log(msg, type)

with open(out_tsvFile, 'w', newline='', encoding='utf-8') as f:
    f.write(Logger.convertToXSV(header, delim))
    iter = 1  # needed for request timeout error
    for page_id in range(firstPage, lastPage + 1):
        try:
            # Forge http request url
            url = "https://www.eolymp.com/en/problems?page=" + str(page_id)
            page = requests.get(url)
            # Initialize the html parser
            soup = BeautifulSoup(page.content, 'html.parser')
            divs = soup.find_all("div", {"class": "eo-list__item eo-problem-row"}) # fetch list
            
            for div in divs:
                try:
                    s = BeautifulSoup(str(div))
                    ids = s.find_all("div", {"class": "eo-problem-row__id eo-problem-row__link_colored"}) # fetch id
                    name = s.find_all("div", {"class": "eo-problem-row__name"}) # fetch name
                    line = [ids[0].text, name[0].text]
                    log("Completed : " + Logger.convertToXSV(line, " : ")[:-1], logger.INFO)
                    f.write(Logger.convertToXSV(line, delim))
                except Exception as e:
                    log(str(e), logger.WARNING)
                    continue
        except Exception as e:
            log(str(e), logger.WARNING)
            continue

