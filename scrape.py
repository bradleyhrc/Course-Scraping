import requests
import time
import smtplib
from bs4 import BeautifulSoup

def email(course: str, section: str, recipient: str) -> None:
    # Set the email server and port
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.connect("smtp.gmail.com", 587)
    server.starttls()

    # removed app password for security
    server.login("htn.fact.checker@gmail.com", "")

    # using old hackathon gmail account that is no longer being used
    sender = "htn.fact.checker@gmail.com"
    subject = f"{course} open spot!"
    body = f"A seat opened up in {course} {section}. Go grab it! :) \n\n- Bradley"

    msg = f"From: {sender}\nTo: {recipient}\nSubject: {subject}\n\n{body}"
    server.sendmail(sender, recipient, msg)

    server.quit() # disconnect

def check_spots(course: str, url: str, notifyID: str) -> None:
    
    # Make a GET request to the website
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    table = soup.find("table").find("table")
    classes = table.find_all("tr")
    classes = classes[1:]
    
    results = []
    
    for c in classes:
        
        # clean results
        if "LEC" not in str(c): continue
        
        # collecting data based on html tags + further cleaning
        c = c.find_all("td")
        c = c[1:2] + c[6:8]
        
        for i in range(len(c)):
            c[i] = str(c[i])

            if not i:
                c[i] = c[i][19:26]
            else:
                c[i] = c[i][19:21]
                c[i] = int(c[i])
        
        results.append(c)

    for sect in results:
        if sect[1] > sect[2]: 
            print('A seat opened up in ' + sect[0] + '!')
            email(course, sect[0], notifyID)
    

if __name__ == "__main__":
    URL1 = "https://classes.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl?level=under&sess=1231&subject=CS&cournum=350"
    URL2 = "https://classes.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl?level=under&sess=1231&subject=CS&cournum=492"
    count = 0

    while True:
        check_spots("CS 350", URL1, "bradleyhrct@gmail.com")
        check_spots("CS 492", URL2, "mik.szuga@gmail.com")

        print("~ Check " + str(count) + " completed.")
        count += 1
        
        time.sleep(9 * 60)  
