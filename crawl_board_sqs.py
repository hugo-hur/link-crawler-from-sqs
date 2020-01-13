import boto3
from selenium import webdriver
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup


queue_url = 'https://sqs.eu-north-1.amazonaws.com/414647029881/CrawlerLinkQueue.fifo'
sqs = boto3.client('sqs', region_name='eu-north-1')
def sendToSQS(link):
    response = sqs.send_message(
            QueueUrl=queue_url,
            MessageGroupId="thread_link",
            DelaySeconds=0,
            MessageBody=link#()
    )
    #print(response)

def crawl_board_to_sqs(sub_board):
    driver = None
    while True:
        try:
            driver = webdriver.Firefox()
            driver.get(sub_board)
            break
        except Exception as e:
            print(str(e))
            print("Web driver exception for sub board " + sub_board)
        
    #threadsOnPage = []
    threads = 0
    pages = 0
    print("Getting thread list at " + sub_board)
    while True:
        #wait = WebDriverWait(driver, 10)#Wait times out after 10 seconds for the next button to appear
        #men_menu = wait.until(ec.visibility_of_element_located((By.XPATH, "//a[@class='next icon-chevron-right']")))
        try:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
        except selenium.common.exceptions.WebDriverException:
            print("Got web driver exception for sub board " + sub_board)
            #Start again
            driver.get(sub_board)
            continue
        #threadsOnPage.extend(soup.find_all("a", {"class":"postsubject"}))
        for link in soup.find_all("a", {"class":"postsubject"}):
            #threadsOnPage.append('https://ylilauta.org' + link.get("href"))#Get the numeric thread url
            #send to sqs
            threads += 1
            sendToSQS('https://ylilauta.org' + link.get("href"))
            
        if soup.find("div", {"class":"infobar"}) == None:#Not last page
            try:
                pages = pages + 1
                driver.find_element_by_xpath("//a[@class='next icon-chevron-right']").click()#Next page
            except Exception as e:
                print(str(e))
                print("Could not find next button at " + sub_board)
                break
        else:
            print("Found no more posts infobar at page " + str(pages + 1) + " at " + sub_board)
            break
    #print("Found " + str(pages) + " pages")
    driver.quit()
    return threads
