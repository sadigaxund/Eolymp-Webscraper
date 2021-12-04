
# Import Required Modules
from bs4 import BeautifulSoup
import requests
import time

out_tsvFile = 'Eolymp.tsv'
delim = '\t'
header = ["ID", "Problem"]

first = 1
last =  10962

def convertToTSV(line):
    retval = line[0]
    for i in range(1, len(line)):
        retval += delim + line[i]
    return retval + "\n"

def scrapePages(starti, endi):
    with open(out_tsvFile, 'w', newline='') as f:
        f.write("ID\tProblem\n")
        iter = 0
        for page_id in range(starti, endi + 1):
            try:
                page = requests.get("https://www.eolymp.com/en/problems/" + str(page_id))
                soup = BeautifulSoup(page.content, 'html.parser')
                page_body = soup.body
                div1 = page_body.select('h1')
                line = str(page_id) + "\t" + div1[0].text
                
                if "Signin" in line:
                    print("Error Writing(Signin) : " + str(page_id))
                    continue

                if "503 Service" in line:
                    iter += 1
                    if iter == 3:
                        iter = 0
                        print("I gave up(Timeout) : " + str(page_id))
                        continue
                    page_id -= 1
                    time.sleep(1)
                    continue

                    
                print("Completed " + str("{:.2f}".format(float(page_id - first) / (last - first + 1) * 100))  + "% : " + div1[0].text )
                f.write(line + "\n")
                
            except Exception as e:
                print(str(e))
                continue
        print("Completed 100.00%")
        f.close()



scrapePages(first, last);

    


