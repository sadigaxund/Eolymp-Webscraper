
# Import Required Modules
from logging import WARNING
from bs4 import BeautifulSoup
from header import LogUtil as Logger
import requests
import time
import sys


logger = Logger('data/info.log')
out_tsvFile = 'data/Eolymp.tsv'
delim = '\t'
header = ["ID", "Problem", "Complexity"]
firstPage = 0
lastPage = 2

# Log helper method
def log(msg, type):
    logger.print(msg, type)
    logger.log(msg, type)

with open(out_tsvFile, 'w', newline='') as f:
    f.write(Logger.convertToXSV(header, delim))
    iter = 1  # needed for request timeout error
    for page_id in range(firstPage, lastPage + 1):
        try:
            # Forge http request url
            url = "https://www.eolymp.com/en/problems?page=" + str(page_id)
            page = requests.get(url)
            # Initialize the html parser
            soup = BeautifulSoup(page.content, 'html.parser')
            divs = soup.find_all("div", {"class": "eo-list__item eo-problem-row"})
            problems = []
            for div in divs:
                s = BeautifulSoup(str(div))
                ids = s.find_all("div", {"class": "eo-problem-row__id eo-problem-row__link_colored"})
                name = s.find_all("div", {"class": "eo-problem-row__name"})
                complx = s.find_all("div", {"class": "eo-problem-row__complexity"})
                line = [ids[0].text, name[0].text, complx[0].text]
                log("Completed : " + Logger.convertToXSV(line, " : "), logger.INFO)
                f.write(Logger.convertToXSV(line, delim))
        except Exception as e:
            print(str(e))
            continue

