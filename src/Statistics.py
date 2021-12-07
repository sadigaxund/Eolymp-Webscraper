
# Import Required Modules
from logging import WARNING
from bs4 import BeautifulSoup
from header import LogUtil as Logger
import requests
import time
import os
p = os.path.abspath('..')

dataPath = str(p) + "\data"
logPath =  dataPath + "\info.log"

logger = Logger(logPath)
out_tsvFile = dataPath + '\statistics_raw.tsv'
delim = '\t'
header = ["ID", "Submits", "Accepted submits", "Users submitted", "Users accepted", "Complexity"]
firstProblem = 1
lastProblem = 10962

# Log helper method
def log(msg, type):
    logger.print(msg, type)
    logger.log(msg, type)

with open(out_tsvFile, 'w', newline='') as f:
    f.write(Logger.convertToXSV(header, delim))
    iter = 1  # needed for request timeout error
    for page_id in range(firstProblem, lastProblem + 1):
        try:
            # Forge http request url
            url = "https://www.eolymp.com/en/problems/" + str(page_id) + "/statistics"
            page = requests.get(url)
            # Initialize the html parser
            soup = BeautifulSoup(page.content, 'html.parser')
            # Fetch header tag which contains the 'problem name'
            div = soup.find_all("div", {"class": "eo-paper__content"}) # fetch list
            text = div[0].text.split("\n")
            for i in range(len(text)):
                text[i] = [s for s in text[i].split() if (s.isdigit() or "%" in s)]
                if len(text[i]) > 0:
                    text[i] = text[i][0]
            text = text[:-2]
            text[0] = page_id # append problem id to the data

            percent = float(page_id - firstProblem + 1) / (lastProblem - firstProblem + 1) * 100
            log("Completed " + str("{:.2f}".format(percent)) + "% : "+ str(page_id), logger.INFO)
            f.write(Logger.convertToXSV(text, delim))
        except Exception as e:
            print(str(e))
            continue
