from selenium import webdriver
import time
import datetime
import bs4
import re


class web_crawler:
    #
    # Constructor
    #

    def __init__(self):

        # Initialize the Driver and go to login Page
        self.driver = webdriver.Chrome(
            "D:\Github_Repos\Weibo Tracker\chromedriver.exe")
        self.cookies = None
        self.main_window = None
        self.driver.get(
            "https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F")

    #
    # Used for logging-in
    #
    def weibo_login(self):

        print("Logging in...")

        try:
            id = self.driver.find_element_by_id("loginName")
            time.sleep(1)

            # Login Processing by ID and Password
            id.send_keys("")
            pw = self.driver.find_element_by_id("")
            pw.send_keys('')

            # Click submit
            submit = self.driver.find_element_by_id('loginAction')
            submit.click()

            # Get the cookies
            self.cookies = self.driver.get_cookies()
            # Save the cookies
            for s_cookie in self.cookies:
                self.driver.add_cookie(s_cookie)

            self.main_window = self.driver.current_window_handle
            time.sleep(5)
            #
            # Start to capture the online status
            #
            self.capture_status()

        except Exception as e:
            print('Was not able to find an element with that name.' + e)

    #
    # Status Capturing
    #
    def capture_status(self):
        while (True):
            time.sleep(5)
            self.driver.get(
                "http://www.weibo.com/aj/user/newcard?id= <<< id >>>>&usercardkey=weibo_mpj&refer_flag=<<< Flag >>>_&type=1&callback=<<<< Callback >>>>")
            bs4_handler = bs4.BeautifulSoup(
                self.driver.page_source, "html.parser")
            status = re.compile("\"W\_chat\_stat W\_chat\_stat\_(.+)\"><\\\\/i>").search(bs4_handler.text).groups()[
                0].replace(
                '\\', "")
            print(
                status + " at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    #
    # Quit the driver
    #
    def quit(self):
        self.driver.quit()


#
# Main
#
if __name__ == '__main__':
    crawler = web_crawler()
    crawler.weibo_login()
