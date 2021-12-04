
# Import Required Modules
from logging import WARNING
from bs4 import BeautifulSoup
from header import LogUtil as Logger
import requests
import time

logger = Logger('data/info.log')
out_tsvFile = 'Eolymp.tsv'
delim = '\t'
header = ["ID", "Problem"]
firstProblem = 1
lastProblem = 10

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
            url = "https://www.eolymp.com/en/problems/" + str(page_id)
            page = requests.get(url)
            # Initialize the html parser
            soup = BeautifulSoup(page.content, 'html.parser')
            # Fetch header tag which contains the 'problem name'
            div1 = soup.body.select('h1')
            # Scraped Data
            line = [page_id, div1[0].text]

            '''
            < Exception Handling >  

            If the response contains 'Signin', 
            the problem is not publicly available
            '''
            if "Signin" in line[1]:
                log("Access Denied, Private Problem : Problem @ " + url, logger.WARNING)
                continue

            if "503 Service" in line[1]:
                iter += 1
                if iter == 4:
                    iter = 1
                    log("Request Timeout : Problem @ " + url, logger.WARNING)
                    continue
                page_id -= 1 # decrease id to return back and try again
                time.sleep(1 + iter) # wait till system can respond
                continue

            if "Page not found" in line[1]:
                log("Page not found : Problem @ " + url, logger.WARNING)
                continue

            percent = float(page_id - firstProblem + 1) / (lastProblem - firstProblem + 1) * 100
            log("Completed " + str("{:.2f}".format(percent)) + "% : "+ str(page_id) + " : " + div1[0].text, logger.INFO)
            f.write(Logger.convertToXSV(line, delim))
        except Exception as e:
            print(str(e))
            continue
