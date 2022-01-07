from sys import exc_info
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common import by
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
#/////////////////////////////////////////////////////////////////////
import win32com.client
# /////////////////////////////////////////////////////////////////////
# Helper functions
# close all tabs
def closeAllTabs(brwsr):
    for handle in brwsr.window_handles:
        brwsr.switch_to.window(handle)
        brwsr.close()
#check login
def login(netID, password):
    print('Trying to login....')
    print('___________________')
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    service_ = Service("chromedriver.exe")
    browser = webdriver.Chrome(service=service_, options=chrome_options)

    browser.set_window_size(1080,1080)
    browser.get('https://my.uic.edu/uPortal/f/welcome/normal/render.uP')
    # navigate to the login button in my.uic.edu
    browser.find_element(By.XPATH,'/html/body/div/div[2]/header/div[1]/div/div/section/div/div/div/div/a').click()
    browser.find_element(By.XPATH,'/html/body/div/main/div/form/fieldset/div/p[1]/input').click()
    browser.find_element(By.XPATH,'/html/body/div/main/div/form/input[1]').click()
    # log in
    browser.find_element(By.NAME,'UserID').send_keys(netID)
    browser.find_element(By.NAME,'password').send_keys(password)
    # select the school and submit
    # (also check if log in was successful)
    try :
        browser.find_element(By.XPATH,'/html/body/div[2]/form/button').click()
        browser.find_element(By.XPATH,"//*[contains(text(), 'Registration/View Classes -  XE Registration')]").click()
    except:
        closeAllTabs(browser)
        print('Login failed, restart and try again...')
        time.sleep(4)
        exit()
    print('Login successful')
    print('___________________')
    time.sleep(.5)
    closeAllTabs(browser)
# /////////////////////////////////////////////////////////////////////
# Initiate the browser
def registrer(CRN_num, netID, password):
    #start the browser
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    service_ = Service("chromedriver.exe")
    browser = webdriver.Chrome(service=service_, options=chrome_options)

    browser.set_window_size(1080,1080)
    browser.get('https://my.uic.edu/uPortal/f/welcome/normal/render.uP')
    # navigate to the login button in my.uic.edu
    browser.find_element(By.XPATH,'/html/body/div/div[2]/header/div[1]/div/div/section/div/div/div/div/a').click()
    browser.find_element(By.XPATH,'/html/body/div/main/div/form/fieldset/div/p[1]/input').click()
    browser.find_element(By.XPATH,'/html/body/div/main/div/form/input[1]').click()
    # log in (assumne that the login() function was ran before this and has comfirmed that the credientials works)
    browser.find_element(By.NAME,'UserID').send_keys(netID)
    browser.find_element(By.NAME,'password').send_keys(password)
    # select the school and submit
    browser.find_element(By.XPATH,'/html/body/div[2]/form/button').click()
    browser.find_element(By.XPATH,"//*[contains(text(), 'Registration/View Classes -  XE Registration')]").click()
    # switch to registration tab and click registration
    browser.implicitly_wait(10)
    reg = browser.window_handles[1]
    browser.switch_to.window(reg)
    # click on the semester
    browser.find_element(By.ID, 'registerLink').click()
    browser.implicitly_wait(100)
    browser.find_element(By.XPATH, '//*[@id="IdPList"]/input[1]').click()
    browser.implicitly_wait(100)
    browser.find_element(By.XPATH, '//*[@id="s2id_txt_term"]').click()
    browser.implicitly_wait(100)
    browser.find_element(By.XPATH, '/html/body/div[8]/ul/li[1]/div').click()
    browser.implicitly_wait(100)
    browser.find_element(By.XPATH,"//*[contains(text(), 'Continue')]").click()
    browser.implicitly_wait(100)
    browser.find_element(By.XPATH, '//*[@id="enterCRNs-tab"]').click()
    # string manipulation for each CRN text field
    crn_txt = '//*[@id="txt_crn1"]'
    #input CRN_num from the passed in
    browser.find_element(By.XPATH, crn_txt).send_keys(str(CRN_num[1:]))
    try:
        #submit
        browser.find_element(By.XPATH, '//*[@id="addCRNbutton"]').click()
        # uncomment the line down below to actually submit it. or do it yourself
        browser.find_element(By.ID, 'saveButton').click()
        print('Yoinked successfully')
    except:
        print('Something went wrong with the CRN: ' + str(CRN_num[1:]))
        print('Please check manually...')
    # Close all tabs when done
    closeAllTabs(browser)
#/////////////////////////////////////////////////////////////////////
# Main:... 
# get user credentials
print("/////////////////////////////////")
netID    = input("NetID   : ")
password = input("Password: ")
print("/////////////////////////////////")
login(netID, password)
print('Waiting for a CRN notification...')
while True:
    ol = win32com.client.Dispatch( "Outlook.Application")
    inbox = ol.GetNamespace("MAPI").GetDefaultFolder(6)
    messages = inbox.Items
    message_current = messages.GetLast()

    if (message_current.UnRead == True) and ('There are open seats or a waitlist space' in message_current.Body):
        message_current.UnRead = False
        CRN = message_current.Body[message_current.Body.find('(CRN: ') + 5:message_current.Body.find('(CRN: ') + 11]
        print ('Adding CRN: ' + CRN)
        try:
            registrer(CRN, netID, password)
        except exc_info:
            print("Error: ", exc_info)
            print("_______________________________________________________")
            print("something went wrong.... but we'll keep the bot alive")
    time.sleep(5)



