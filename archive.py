'''
(c) 2023 Gregory Karastergios

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
'''

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

    i = 0
    SCREENSHOT_COUNT = 100

    CURRENT_DATETIME = datetime.now()
    CURRENT_TIME = CURRENT_DATETIME.strftime("%Y-%m-%d_%H-%M-%S")
    UNIX_TIME = time.mktime(CURRENT_DATETIME.timetuple())

    while i < SCREENSHOT_COUNT:
        SCREENSHOT_FILENAME = "{}_{}_{}.png".format(ACCOUNT, CURRENT_TIME, i)
        print(SCREENSHOT_FILENAME)
        driver.save_screenshot(filename=SCREENSHOT_FILENAME)
        webdriver.ActionChains(driver).scroll_by_amount(0, 1000).perform()

        i += 1
    driver.quit()


if __name__ == '__main__':
    main()