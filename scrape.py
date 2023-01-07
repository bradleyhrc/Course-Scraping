import requests
import time
from bs4 import BeautifulSoup

def main(count: int) -> None:
    url = "https://classes.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl?level=under&sess=1231&subject=CS&cournum=350"

    # Make a GET request to the website
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    table = soup.find("table").find("table")
    classes = table.find_all("tr")
    classes = classes[1:]

    results = []

    # Print the main content
    for c in classes:
        c = c.find_all("td")
        c = c[1:2] + c[6:8]

        for i in range(len(c)):
            c[i] = str(c[i])

            if not i:
                c[i] = c[i][19:26]
            else:
                c[i] = c[i][19:21]
                c[i] = int(c[i])
        
        if c[0] != 'TST 101': results.append(c)

    #print(results)

    for sect in results:
        if sect[1] > sect[2]: print('A seat opened up in ' + sect[0] + '!')

    print("~ Check " + str(count) + " completed.")

if __name__ == "__main__":
    count = 0
    while count < 10:
        main(count)
        time.sleep(8 * 60)
        count += 1
