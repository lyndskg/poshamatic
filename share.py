import time
import argparse
import sys
import os
import textwrap
import numpy as np
import pyautogui
import logging
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium import webdriver
from webdriver_manager.microsoft import EdgeDriverManager
from selenium.common.exceptions import NoSuchElementException

# Configure the logger
logging.basicConfig(
    filename='share.log',  # Specify the log file name
    level=logging.DEBUG, # Set the logging level to DEBUG or higher
    format='[%(levelname)s] %(asctime)s - %(message)s') # Specify the log message format
)
logger = logging.getLogger(__name__)

# Constants for web drivers
DRIVER_CHROME = 0
DRIVER_SAFARI = 1
DRIVER_FIREFOX = 2
DRIVER_EDGE = 3

def get_webdriver(driver_name):
    try:
        if driver_name == '0' or driver_name.lower() == 'chrome':
            chrome_options = ChromeOptions()
            driver = webdriver.Chrome(options=chrome_options)
        elif driver_name == '1' or driver_name.lower() == 'safari':
            safari_options = SafariOptions()
            driver = webdriver.Safari(options=safari_options)
        elif driver_name == '2' or driver_name.lower() == 'firefox':
            firefox_options = FirefoxOptions()
            driver = webdriver.Firefox(options=firefox_options)
        elif driver_name == '3' or driver_name.lower() == 'edge':
            edge_options = EdgeOptions()
            driver = webdriver.Edge(executable_path=EdgeDriverManager().install(), options=edge_options)
        else:
            raise ValueError("Driver argument value not supported! Check the help (-h) argument for supported values.")
        return driver
    except Exception as e:
        logger.error("Error occurred while initializing the driver: %s", e)
        sys.exit(1)



def setup_driver(driver_name):
    return get_webdriver(driver_name)


# Add the manual_captcha_handler function
def manual_captcha_handler():
    logging.info("[*] ERROR in Share : Thwarted by Captchas")
    logging.info("[*] Please open the browser to the Poshmark login page.")
    logging.info("[*] Solve the CAPTCHA and log in as a human.")
    logging.info("[*] Once you've successfully logged in, come back here.")
    logging.info("[*] Press Enter to continue the script after solving the CAPTCHA.")
    
    # Wait for the user to press Enter to continue
    input("[*] If you want to quit, enter 'q' and press Enter.")

    # Check if the user wants to quit the script
    quit_choice = input().lower().strip()
    if quit_choice == 'q':
        logging.info("[*] Exiting the script.")
        sys.exit()

# Add the offer_user_quit function
def offer_user_quit():
    quit_mes = textwrap.dedent('''
        [*] if you would like to quit, enter [q]
            otherwise, enter any other key to continue
    ''')
    quit_selection = input(quit_mes)
    qs = str(quit_selection).lower()
    if qs == 'q':
        global quit_input
        quit_input = True
    else:
        pass

        
# Modify the login function
def login(debugger=False):

    if debugger is True:
        import pdb; pdb.set_trace()
    else:
        pass

    url = "https://poshmark.com/login"
    driver.get(url)

    time.sleep(get_random_delay(5))

    try:
        ## Login
        logging.info(textwrap.dedent('''
            [*] logging into Poshmark seller account: {}...
                the share war will begin momentarily...
            '''.format(poshmark_username)))
        username = driver.find_element_by_name("login_form[username_email]")
        username.send_keys(poshmark_username)
        time.sleep(get_random_delay(5))

        password = driver.find_element_by_name("login_form[password]")
        password.send_keys(poshmark_password)
        time.sleep(get_random_delay(5))

        password.send_keys(Keys.RETURN)
        time.sleep(get_random_delay(5))
    
        ## Check for Captcha
        try:
            captcha_pat = "//span[@class='base_error_message']"
            captcha_fail = driver.find_element_by_xpath(captcha_pat)
            if len(str(captcha_fail)) > 100:
                logging.info("Captcha detected. Manual intervention required.")
                manual_captcha_handler()  # Call the manual_captcha_handler function
                login(debugger=True)  # Retry login after manual intervention
                return
        except NoSuchElementException:
            pass


        # Existing code...

    except Exception as e:
        # Captcha Catch
        logging.info("[*] ERROR in Share Bot: Thwarted by Captchas")
        logger.error("Error occurred during login: %s", e)
        offer_user_quit()
        login(debugger=True)
        pass
        # Existing code...

    except: Exception:
        # Captcha Catch
        logging.info("[*] ERROR in Share Bot: Thwarted by Captchas")
        offer_user_quit()
        login(debugger=True)
        pass

        ## Navigate to Seller Page
        time.sleep(get_random_delay(10))
        seller_page = get_seller_page_url(args.account)
        driver.get(seller_page)


        ## Confirm Account to Share If Not Username
        if args.bypass == True:
            pass
        else:
            if args.account != poshmark_username:
                confirm_account_sharing(args.account, poshmark_username)
                if quit_input is True:
                    return False
                else:
                     pass
            else:
                pass

        return True

    except:
        ## Captcha Catch
        logging.info(textwrap.dedent('''
            [*] ERROR in Share Bot: Thrwarted by Captchas
                you may now attempt to login with the python debugger
            '''))
        offer_user_quit()
        login(debugger=True)
        pass


def deploy_share_bot(driver, n=3, order=True, random_subset=0):
    logging.info("[*] DEPLOYING SHARE BOT")
    
    try:
        if login() is True:
            pass
        else:
            return

        scroll_page(n)

        ## Share Icons and Order
        share_icons = get_closet_share_icons()

        if order is True:
            share_icons.reverse()
        else:
            pass

        ## Share Random Subset of Items
        if random_subset != 0:
            try:
                random_subset = int(random_subset)
                print(textwrap.dedent('''
                    [*] you have selected to share a random subset of {} items
                        from all {} PoshMark listings in the closet...
                        please wait...
                    '''.format(random_subset, len(share_icons))))

                share_icons = np.random.choice(share_icons, random_subset, replace=False).tolist()

            except Exception as e:
                logger.warning("Error occurred while selecting random subset: %s", e)
                pass
        else:
            pass

        ## Share Message
        logging.info(textwrap.dedent('''
            [*] sharing PoshMark listings for {} items in closet...
                please wait...
            '''.format(len(share_icons))))
    
        
        ## Share Listings using Chrome driver
        for item in share_icons:
            clicks_share_followers(item)
            # Access the requests captured by selenium-wire for Chrome
            for request in chrome_driver.requests:
                if request.response:
                    logging.info(request.url)
                    logging.info(request.method)
                    logging.info(request.response.status_code)
                    logging.info(request.response.headers)
                    

        # Access the requests captured by selenium-wire for Safari
            for request in safari_driver.requests:
                if request.response:
                    logging.info(request.url)
                    logging.info(request.method)
                    logging.info(request.response.status_code)
                    logging.info(request.response.headers)

        ## Share Listings using Firefox driver
        for item in share_icons:
            clicks_share_followers(item)
            # Access the requests captured by selenium-wire for Firefox
            for request in firefox_driver.requests:
                if request.response:
                    logging.info(request.url)
                    logging.info(request.method)
                    logging.info(request.response.status_code)
                    logging.info(request.response.headers)
                    
        # Access the requests captured by selenium-wire for Edge
            for request in edge_driver.requests:
                if request.response:
                    logging.info(request.url)
                    logging.info(request.method)
                    logging.info(request.response.status_code)
                    logging.info(request.response.headers)

            logging.info("[*] closet successfully shared...posh-on...")
        pass
        
    except Exception as e:
        logging.info("[*] ERROR in Share Bot")
        logger.error("Error occurred during share war deployment: %s", e)
        pass

    ## Closing Message
    loop_delay = int(random_loop_time/60)
    current_time = time.strftime("%I:%M%p on %b %d, %Y")
    print(textwrap.dedent('''
        [*] the share war will continue in {} minutes...
            current time: {}
        '''.format(loop_delay, current_time)))
     logging.info(textwrap.dedent('''
        [*] the share war will continue in {} minutes...
            current time: {}
        '''.format(loop_delay, current_time)))




# Add the simulate_human_interaction function
def simulate_human_interaction():
    try:
        # Simulate mouse movement
        x, y = pyautogui.position()
        pyautogui.moveTo(x + 10, y + 10, duration=0.5)
        pyautogui.moveTo(x - 10, y - 10, duration=0.5)
        pyautogui.moveTo(x, y, duration=0.5)

        # Scroll up and down
        pyautogui.scroll(3)
        time.sleep(2)
        pyautogui.scroll(-3)
    except Exception as e:
        logger.warning("Error occurred during simulating human interaction: %s", e)
        pass
   
def get_random_delay(mean_delay):
    times = np.random.rand(1000) + np.random.rand(1000) + mean_delay
    return np.random.choice(times, 1).tolist()[0]



def confirm_account_sharing(account, username):

        ## Get User Input
        logging.info(textwrap.dedent('''
            [*] you have requested to share
                the items in another poshmark closet:
                ------------------------------------
                [*]: {}
                ------------------------------------
            '''.format(account)))
        confirm_mes = (textwrap.dedent('''
            [*] to confirm this request, enter [y]
                to cancel and share your closet items instead enter [n] :
            '''))

        confirm_selection = input(confirm_mes)
        cs = str(confirm_selection).lower()
        if cs == 'y':
            pass
        elif cs == 'n':
            ## Redirect to users's closet page
            seller_page = get_seller_page_url(username)
            driver.get(seller_page)
        else:
            logging.info('[*] you have entered an invalid selection...')
            offer_user_quit()
            if quit_input is True:
                pass
            else:
               confirm_account_sharing(account, username)



def get_seller_page_url(poshmark_account):
    url_stem = 'https://poshmark.com/closet/'
    available = '?availability=available'
    url = '{}{}{}'.format(url_stem, poshmark_account, available)
    return url


def scroll_page(n, delay=3):
    try:
        scroll = 0
        screen_heights = [0]
    
        logging.info("[*] scrolling through all items in closet...")
    
        for i in range(1, n+1):
            scroll +=1
            scroll_script = "window.scrollTo(0, document.body.scrollHeight);"
            driver.execute_script(scroll_script)
            height = driver.execute_script("return document.documentElement.scrollHeight")
            last_height = screen_heights[-1:][0]
    
            if height == last_height:
                return
            else:
                screen_heights.append(height)
                time.sleep(get_random_delay(delay))
    except Exception as e:
        logger.warning("Error occurred during page scrolling: %s", e)
        pass


def get_closet_urls():
    items = driver.find_elements_by_xpath("//div[@class='item-details']")
    urls = [i.find_element_by_css_selector('a').get_attribute('href') for i in items]
    return urls


def get_closet_share_icons():
    def get_closet_share_icons():
    try:
        item_pat = "//div[@class='social-info social-actions d-fl ai-c jc-c']"
        items = driver.find_elements_by_xpath(item_pat)
        share_icons = [i.find_element_by_css_selector("a[class='share']") for i in items]
        return share_icons
    except Exception as e:
        logger.error("Error occurred while getting closet share icons: %s", e)
        return []



def clicks_share_followers(share_icon, d=4.5):

    ## First share click
    driver.execute_script("arguments[0].click();", share_icon); time.sleep(get_random_delay(d))

    ## Second share click
    share_pat = "//a[@class='pm-followers-share-link grey']"
    share_followers = driver.find_element_by_xpath(share_pat)
    driver.execute_script("arguments[0].click();", share_followers); time.sleep(get_random_delay(d))


def open_closet_item_url(url):
    logging.info(url)
    driver.get(url)
    time.sleep(get_random_delay(5))


def main_loop(driver, loop_time, number, order, random_subset, account, bypass):
    while True:
        try:
            # Start Share Bot Loop
            quit_input = False
            deploy_share_bot(driver, number, order, random_subset)

            if quit_input:
                break

            time.sleep(get_random_delay(10))

            # Time Delay: While Loop
            random_loop_time = random(loop_time)
            time.sleep(random_loop_time - ((time.time() - starttime) % random_loop_time))

        except NoSuchElementException as e:
            # Handle NoSuchElementException
            logger.error("Element not found: %s", e)
            offer_user_quit()
            if quit_input:
                driver.quit()
                sys.exit()
            else:
                pass
                
        except Exception as e:
            # Handle other exceptions
            logger.error("ERROR: %s", e)
            offer_user_quit()
            if quit_input:
                pass
            else:
                # Sleep for some time before retrying
                time.sleep(30)

    
if __name__=="__main__":

    
    ##################################
    ## Arguments for Script
    ##################################

    ## Default Arguments with RawTextHelpFormatter
    class RawTextArgumentDefaultsHelpFormatter(
            argparse.ArgumentDefaultsHelpFormatter,
            argparse.RawTextHelpFormatter
        ):
            pass

    ## Check to ensure user has created the credentials.py file
    exists = os.path.isfile('./credentials.py')
    if not exists:
        logging.info(textwrap.dedent('''
            [*] ERROR: `credentials.py` file does not exist.
                You may need to create the file, for example, 
                by copying `example_credentials.py`...

            [*] In terminal, enter the following command:
                cp example_credentials.py credentials.py

            [*] Then edit credentials.py with your
                poshmark closet and password.
                '''))
        sys.exit()
    else:
        import credentials


    ## Fail gracefully if the username or password not specified
    try:
        poshmark_username = credentials.poshmark_username
        poshmark_password = credentials.poshmark_password
    except AttributeError:
        logging.info(textwrap.dedent('''
            [*] ERROR: Username and/or password not specified...
            [*] You may need to uncomment poshmark_username and 
                poshmark_password in credentials.py
            '''))
        sys.exit()

    ## Poshmark closet URL only works with username, so verify
    ## that the user is not using their email address to log in.
    if '@' in poshmark_username:
        logging.info(textwrap.dedent('''
                    [*] Do not your user email address to log in...
                        use your Poshmark username (closet) instead...
                    '''))
        sys.exit()


    parser = argparse.ArgumentParser(
        description=textwrap.dedent('''
        [*] Help file for share.py
            from the poshmark_sharing repository:
            https://github.com/jmausolf/poshmark_sharing
        '''),
        usage='use "python %(prog)s --help" for more information',
        formatter_class=RawTextArgumentDefaultsHelpFormatter)
    parser.add_argument("-t", "--time", default=14400, type=float,
        help=textwrap.dedent('''\
            loop time in seconds to repeat the code

            :: example, repeat in two hours:
            -t 7200
            '''))
    parser.add_argument("-n", "--number", default=1000, type=int,
        help="number of closet scrolls")
    parser.add_argument("-o", "--order", default=True, type=bool, 
        help="preserve closet order")
    parser.add_argument("-r", "--random_subset", default=0, type=int, 
        help="select a random subset (number) of items to share")
    parser.add_argument("-a", "--account", default=poshmark_username, 
        type=str,help=textwrap.dedent('''\
            the poshmark closet account you want to share
            (default is the login account in credentials.py)

            :: example, share another user's closet items:
            -a another_username
            '''))
    parser.add_argument("-b", "--bypass", default=False, type=bool, 
        help=textwrap.dedent('''\
            option to bypass user confirmation
            by default, if the account to be shared is not equal
            to the poshmark username, the user will be prompted to 
            confirm this selection

            :: example, bypass user confirmation
            -b True
            '''))
    parser.add_argument("-d", "--driver", default='0', type=str, 
        help=textwrap.dedent('''\
            selenium web driver selection
            drivers may be called by either entering the name
            of the driver or entering the numeric code 
            for that driver name as follows:
            Chrome==0, Safari==1, Firefox==2, Edge==3

            :: example, use Firefox:
            -d Firefox 
            -d 2

            :: example, use Chrome:
            -d Chrome
            -d 0
            '''))

    args = parser.parse_args()

    ##################################
    ## Set up Webdriver
    ##################################
   
    try:
        driver = get_webdriver(args.driver)
    except ValueError as e:
        logger.error("ERROR: %s", e)
        sys.exit()

    main_loop(driver, args.time, args.number, args.order, args.random_subset, args.account, args.bypass)

    driver.quit()
    sys.exit()
       

