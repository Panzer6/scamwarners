# ---------------------------------------------------------------------------------------------------------------------------------------------
# Code written by: Ronald Andrew Ganotisi (TR-PH-INTRN)
# Last Update: 01/25/23 12:58 AM
# ---------------------------------------------------------------------------------------------------------------------------------------------

from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import time
import requests
from datetime import datetime, timedelta

def check_for_link():
    global end
    if last_email.strip() in cm:
        print("last email discovered.\n")
        rewrite()
        end = time.time() - start
        print(f"\nTime Elapsed: {end:.2f} seconds")
        quit()

def check_for_date():
    global new, repeat
    for link in links:
        if datetimestr in link.text:
            new = True
            repeat = 0

def rewrite():
    global endpoint
    with open("financial.txt", "r") as f:
        endpoint = f.readline()
        f.close()
    with open("last_email.txt", "w") as f:
        print(f"writing {endpoint} to last_email.txt\n")
        f.write(endpoint)
        f.close()

def check_if_repeat():
    global date_now, url, repeat, changes, page_num
    if repeat == 1:
        repeat = 2
        print("\nStill no new links found. Going to next page.\n")
        page_num += 50
        date_now = datetime.now() - timedelta(changes)
        url = f"https://www.scamwarners.com/forum/viewforum.php?f=7&start={page_num}"
        time.sleep(1)
    elif repeat == 2:
        changes += 1
        print("\nStill no new links found. Moving to previous date and recollecting...")
        date_now = datetime.now() - timedelta(changes)
        time.sleep(1)
    else:
        changes += 1
        print("\nNo new links found. Moving to previous date and previous page.\n")
        date_now = datetime.now() - timedelta(changes)
        page_num -= 50
        url = f"https://www.scamwarners.com/forum/viewforum.php?f=7&start={page_num}"
        repeat = 1
        time.sleep(1)

start = time.time()
temp = ""
date_now = datetime.now()
url = "https://www.scamwarners.com/forum/viewforum.php?f=7"
last_email = ""
page_num = 0
num = 0
new = False
changes = 0
repeat = 0

with open("last_email.txt", "r") as f:
    last_email = f.readline()
    print(f"Scraper will stop when encountering: {last_email}")
    f.close()
open("financial.txt", "w").close()
driver = uc.Chrome()
while True:
    driver.get(url)
    datetimestr = date_now.strftime("%b %d, %Y")
    page_source = driver.page_source
    contents = BeautifulSoup(page_source, "lxml")
    rtable = contents.find("table", class_="footable table table-striped table-bordered table-white table-primary table-hover")
    links = contents.find_all("tr", class_="")
    sample = "Jan 31, 2023"
    new = False
    check_for_date()
    if new == True:
        for link in links:
            if datetimestr in link.text:
                email = link.find("a", class_="topictitle")
                temp = email.text.strip()
                cmp = temp.split(" ")
                for cm in cmp:
                    if "@" in cm:
                        check_for_link()
                        with open("financial.txt", "a") as f:
                            num+=1
                            f.write(cm + "\n")
                            print(f"Found {num} emails")
                            f.close()
                    else:
                        continue 
        page_num += 50
        url = f"https://www.scamwarners.com/forum/viewforum.php?f=7&start={page_num}"
        print(f"\nDone checking page {int(page_num/50)} for emails on {datetimestr}")
        print("\nOn to the next page...")
        time.sleep(1)
    else:
        if page_num <= 0:
            changes += 1
            print("\nNo new links found. Moving to previous date and recollecting...")
            date_now = datetime.now() - timedelta(changes)
            time.sleep(1)
        else:
            check_if_repeat()     