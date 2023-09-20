from selenium import webdriver
import time
from datetime import datetime
import sys
import os
import json

COOKIE_FILE_PATH = '.secrets/twitter.com_cookies.txt'
WIDTH = 1080
HEIGHT = 1920

def escape_slashes(input):
    return input.replace("\"", "\\\"")
    

def main():

    # Start the headless browser
    ACCOUNT = sys.argv[1]
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    #options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(WIDTH, HEIGHT)
    
    driver.get("http://twitter.com/" + ACCOUNT)
    cookie_f = open(COOKIE_FILE_PATH, 'r')
    lines = cookie_f.readlines()

    # Add the session cookie
    for line in lines:
        cookie = {}
        line_spl = line.split("\t")

        if (len(line_spl) >= 7):
            cookie["name"] = escape_slashes(line_spl[5])
            cookie["value"] = escape_slashes(line_spl[6][:-1])
            cookie["domain"] = "twitter.com"

            #print(cookie)
            driver.add_cookie(cookie)

    cookie_f.close()

    # Reload the page with the session cookie
    driver.refresh()

    # driver.implicitly_wait(30)
    time.sleep(5)

    os.chdir("archive")

    if (os.path.isdir(ACCOUNT) == False):
        os.mkdir(ACCOUNT)

    os.chdir(ACCOUNT)

    CURRENT_DATETIME = datetime.now()
    UNIX_TIME = time.mktime(CURRENT_DATETIME.timetuple())
    driver.save_screenshot(filename="{}_header_{}.png".format(ACCOUNT, round(UNIX_TIME)))
    driver.quit()


if __name__ == '__main__':
    main()