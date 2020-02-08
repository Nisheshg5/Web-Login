import os
import ctypes
import threading
from time import ctime
from builtins import print as pr
from subprocess import check_output
from selenium.webdriver import Chrome

# from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
from ChromeVersion import chrome_browser_version, nextVersion, lastVersion


class Login_Thread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        """
            Will check wheather the portal in logged in after a set interval and will sign in if not. 
        """
        try:

            # set the arguments and options
            chromeOptions = Options()
            prefs = {"profile.managed_default_content_settings.images": 2}
            chromeOptions.add_experimental_option("prefs", prefs)
            chromeOptions.add_experimental_option("excludeSwitches", ["enable-logging"])
            chromeOptions.add_argument("--headless")
            chromeOptions.add_argument("--blink-settings=imagesEnabled=false")
            chromeOptions.add_argument("--disable-popup-blocking")
            chromeOptions.add_argument("--ignore-certificate-errors")
            chromeOptions.add_argument("--allow-insecure-localhost")
            chromeOptions.add_argument("--allow-running-insecure-content")
            chromeOptions.accept_untrusted_certs = True
            chromeOptions.assume_untrusted_cert_issuer = True
            service_args = ["hide_console"]
            currentPath = (
                os.path.dirname(os.path.abspath(__file__))
                + "\\ChromeDriver\\"
                + chrome_browser_version
                + "\\chromedriver.exe"
            )

            while True:
                try:
                    print("\nCalling Driver")

                    # Creating an instance of chrome
                    driver = Chrome(
                        executable_path=currentPath,
                        options=chromeOptions,
                        service_args=service_args,
                    )
                    print("Driver Called")
                    driver.set_page_load_timeout(10)
                    driver.delete_all_cookies()

                    # open a page
                    driver.get("Enter Checking Site Here")
                    print("Getting Site")
                    try:
                        """
                        
                            remove this try except if the your wifi doesn't block websites
                        
                        """

                        # xpath if the website is blocked
                        element = driver.find_element_by_xpath(
                            "Enter xpath to an element in the blocked page"
                        )
                        print("Site Blocked\n")

                    except:
                        try:
                            # xpath to any thing in the website to make sure you are connected to the internet
                            element = driver.find_element_by_xpath(
                                "/Enter xpath to an element in the page"
                            )
                            print("Site Opening\n")

                        except:
                            try:
                                """
                                
                                    if your portal doesn't have auto redirect, uncomment the following line and type in your login url
                                
                                """

                                # driver.get("Paste Login Webiste URL Here")

                                # change the ids to those in your login website
                                # you can use developer mode to find the id of fields (use ctrl + shift + i)
                                # change the username and password to the required one
                                print("Trying To Login")
                                # select usnername field
                                element = driver.find_element_by_id("Ending id of user input field")
                                print("User Found")
                                element.send_keys("Enter username")
                                print("User Inputted")
                                # select password field
                                element = driver.find_element_by_id("Ending id of password input field")
                                print("Passwprd Found")
                                element.send_keys("Enter password")
                                print("Password Inputted")
                                # select submit button
                                element = driver.find_element_by_id("Enter id of submit button")
                                print("Button Found")
                                element.click()
                                print("Logged In\n")
                            # except NoSuchElementException as ex:
                            #     print("Can't Login")
                            #     event.wait(120)
                            except Exception as ex:
                                print(
                                    "Can't login:\t\tAn exception of type {0} occurred. Arguments:\n{1}".format(
                                        type(ex).__name__, ex.args
                                    )
                                )
                                event.wait(60)
                                continue

                except Exception as ex:
                    print(
                        "Error in loop:\t\tAn exception of type {0} occurred. Arguments:\n{1}".format(
                            type(ex).__name__, ex.args
                        )
                    )
                    try:
                        driver.quit()
                    except Exception as ex:
                        print(
                            "Error in Quitting:\t\tAn exception of type {0} occurred. Arguments:\n{1}".format(
                                type(ex).__name__, ex.args
                            )
                        )

                    event.wait(60)
                    continue

                try:
                    driver.quit()
                except Exception as ex:
                    print(
                        "Error in Quitting in loop:\t\tAn exception of type {0} occurred. Arguments:\n{1}".format(
                            type(ex).__name__, ex.args
                        )
                    )
                event.wait(300)
                continue

        except Exception as ex:
            print(
                "Error outside loop:\t\tAn exception of type {0} occurred. Arguments:\n{1}".format(
                    type(ex).__name__, ex.args
                )
            )

        finally:
            try:
                driver.quit()
            except Exception as ex:
                print(
                    "Error in Quitting in final:\t\tAn exception of type {0} occurred. Arguments:\n{1}".format(
                        type(ex).__name__, ex.args
                    )
                )
            # print("\n" + "ended")

    def get_id(self):
        """ 
            Returns id of the respective thread. 
        """
        if hasattr(self, "_thread_id"):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    # stop the thread when the raise exception is called
    def raise_exception(self):
        """
            Will raise an exception and stop the thread.
        """
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            thread_id, ctypes.py_object(SystemExit)
        )
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print("Exception raise failure")


class Update_Thread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    # target function of the thread class
    def run(self):
        try:
            import os

            driverName = "\\chromedriver.exe"

            # defining base file directory of chrome drivers
            driver_loc = os.path.dirname(os.path.abspath(__file__)) + "\\ChromeDriver\\"

            # defining the file path of your exe file automatically updating based on your browsers current version of chrome.
            currentPath = driver_loc + chrome_browser_version + driverName

            # check if new version of drive exists --> only continue if it doesn't
            Newpath = driver_loc + nextVersion

            # check if we have already downloaded the newest version of the browser
            newfileloc = Newpath + driverName
            newpathexists = os.path.exists(newfileloc)

            if newpathexists == False:
                try:
                    # open chrome driver and attempt to download new chrome driver exe file.

                    # set the arguments and options
                    chromeOptions = Options()
                    chromeOptions.add_experimental_option(
                        "prefs",
                        {
                            "download.default_directory": driver_loc,
                            "download.prompt_for_download": False,
                            "download.directory_upgrade": True,
                            "safebrowsing.enabled": True,
                            "profile.managed_default_content_settings.images": 2,
                        },
                    )
                    chromeOptions.add_experimental_option(
                        "excludeSwitches", ["enable-logging"]
                    )
                    chromeOptions.add_argument("--headless")
                    chromeOptions.add_argument("--blink-settings=imagesEnabled=false")
                    chromeOptions.add_argument("--disable-popup-blocking")
                    chromeOptions.add_argument("--ignore-certificate-errors")
                    chromeOptions.add_argument("--allow-insecure-localhost")
                    chromeOptions.add_argument("--allow-running-insecure-content")
                    chromeOptions.accept_untrusted_certs = True
                    chromeOptions.assume_untrusted_cert_issuer = True
                    service_args = ["hide_console"]

                    try:
                        print("~~~Calling Update Driver")
                        update_driver = Chrome(
                            executable_path=currentPath,
                            options=chromeOptions,
                            service_args=service_args,
                        )
                        print("~~~Update Driver Opened")

                        # opening up url of chromedriver to get new version of chromedriver.
                        chromeDriverURL = (
                            "https://chromedriver.storage.googleapis.com/index.html?path="
                            + nextVersion
                        )
                        update_driver.set_page_load_timeout(5)
                        update_driver.delete_all_cookies()
                        update_driver.get(chromeDriverURL)
                        print("~~~Update Website Got")

                        # time.sleep(5)
                        event.wait(5)
                        # find records of table rows
                        table = update_driver.find_elements_by_css_selector("tr")

                        # check the length of the table
                        Table_len = len(table)

                        # ensure that table length is greater than 4, else fail. -- table length of 4 is default when there are no availble updates
                        if Table_len > 4:

                            # define string value of link
                            rowText = table[(len(table) - 2)].text[:6]
                            # time.sleep(1)
                            event.wait(1)

                            # select the value of the row
                            update_driver.find_element_by_xpath(
                                "//*[contains(text()," + '"' + str(rowText) + '"' + ")]"
                            ).click()
                            event.wait(1)
                            # time.sleep(1)

                            # select chromedriver zip for windows
                            update_driver.find_element_by_xpath(
                                "//*[contains(text()," + '"' + "win32" + '"' + ")]"
                            ).click()
                            print("~~~Download Started")

                            # time.sleep(5)
                            event.wait(5)
                            update_driver.quit()

                            print("~~~Update Driver Exited")

                            try:
                                from zipfile import ZipFile
                                import shutil

                                fileName = os.path.join(
                                    os.path.dirname(driver_loc),
                                    "chromedriver_win32.zip",
                                )

                                # Create a ZipFile Object and load sample.zip in it
                                with ZipFile(fileName, "r") as zipObj:
                                    # Extract all the contents of zip file in different directory
                                    zipObj.extractall(Newpath)

                                print("~~~Newer Version Extracted")
                            except Exception as ex:
                                print(
                                    "Error in extracting:\t\tAn exception of type {0} occurred. Arguments:\n{1}".format(
                                        type(ex).__name__, ex.args
                                    )
                                )

                            try:
                                # delete downloaded file
                                os.remove(fileName)
                                print("Downloaded Zip Deleted")
                            except Exception as ex:
                                print(
                                    "~~~Error in deleting zip:\t\tAn exception of type {0} occurred. Arguments:\n{1}".format(
                                        type(ex).__name__, ex.args
                                    )
                                )

                            # defining old chrome driver location
                            oldPath = driver_loc + lastVersion
                            oldpathexists = os.path.exists(oldPath)

                            # this deletes the old folder with the older version of chromedriver in it
                            if oldpathexists == True:
                                try:
                                    import stat

                                    shutil.rmtree(oldPath, ignore_errors=True)

                                    print("Old Version Deleted")
                                except Exception as ex:
                                    print(
                                        "~~~Error in deleting previous version:\t\tAn exception of type {0} occurred. Arguments:\n{1}".format(
                                            type(ex).__name__, ex.args
                                        )
                                    )

                        else:
                            # update_driver.quit()
                            print("~~~No new version available")

                    except Exception as ex:
                        print(
                            "~~~Error in update driver:\t\tAn exception of type {0} occurred. Arguments:\n{1}".format(
                                type(ex).__name__, ex.args
                            )
                        )

                    finally:
                        try:
                            # close the driver
                            update_driver.quit()
                            print("~~~Update Driver Exited")
                        except Exception as ex:
                            print(
                                "~~~Error in quitting:\t\tAn exception of type {0} occurred. Arguments:\n{1}".format(
                                    type(ex).__name__, ex.args
                                )
                            )
                except Exception as ex:
                    print(
                        "~~~Error in if:\t\tAn exception of type {0} occurred. Arguments:\n{1}".format(
                            type(ex).__name__, ex.args
                        )
                    )
            else:
                print("~~~ChromeDriver Upto Date~~~")

        except Exception as ex:
            print(
                "~~~Error in update:\t\tAn exception of type {0} occurred. Arguments:\n{1}".format(
                    type(ex).__name__, ex.args
                )
            )

    def get_id(self):
        """ 
            Returns id of the respective thread. 
        """
        if hasattr(self, "_thread_id"):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    # stop the thread when the raise exception is called
    def raise_exception(self):
        """
            Will raise an exception and stop the thread.
        """
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            thread_id, ctypes.py_object(SystemExit)
        )
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print("Exception raise failure")


# write the unbuffered output to log file instead of terminal
def print(*args, **argv):
    for arg in args:
        ar = str(arg).split("\n")
        for line in ar:
            if line.strip() == "":
                pr("", sep="", **argv, file=log_file, flush=True)
                # pr("", sep="", **argv)
            else:
                pr(
                    "[" + ctime() + "]" + "\t\t",
                    line,
                    sep="",
                    **argv,
                    file=log_file,
                    flush=True
                )
                # pr(
                #     "[" + ctime() + "]" + "\t\t",
                #     line,
                #     sep="",
                #     **argv
                # )
    # pr("["+ctime()+"]" + "\t\t",*args, sep=" ", **argv, file=log_file, flush=True)
    # pr(*args, sep=" ", end="\n", flush=True)


# file object of log file
log_file = open(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "log.log"),
    "w",
    encoding="utf-8",
)


print("Started\n")


# path to close file
close = os.path.join(os.path.dirname(os.path.abspath(__file__)), "close.txt")

# event object needed to use wait
event = threading.Event()


# close an existing instance of script
with open(close, "w", encoding="utf-8") as f:
    f.write("1")
event.wait(5)

# reset the close file
with open(close, "w", encoding="utf-8") as f:
    f.write("0")


# thread which does the main work
thread = Login_Thread("Thread 1")
thread.start()

# thread to update the chromedriver
update_Thread = Update_Thread("Thread 2")
update_Thread.start()


# stop the thread when the close file changes
while True:
    with open(close, "r", encoding="utf-8") as f:
        if f.read() == "1":
            print("Ending")
            event.set()
            thread.raise_exception()
            update_Thread.raise_exception()
            break
    event.wait(3)

# wait for the threads to end
thread.join()
update_Thread.join()


print("\nENDED")
