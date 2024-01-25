#!/usr/bin/python3
#Web scraper for kcnawatch.nknews.org

#/html/body/div[1]/div/div[7]/div/div[1]/div[2]/small
#/html/body/div[1]/div/div[26]/div/div[1]/div[2]/small
#the dates 7-26 inclusive
        
#/html/body/div[1]/div/div[7]/div/div[2]/div[1]/a
#/html/body/div[1]/div/div[26]/div/div[2]/div[1]/a
#the titles 7-26 inclusive
        
#/html/body/div[1]/div/div[5]/div[1]/h2
#/html/body/div[1]/div/div[5]/div[1]/article/p
#the title/article after following the link

import time
from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import enchant

start_time = time.time()
browser = webdriver.Firefox()
page = 1
url = "http://kcnawatch.nknews.org/site/jp/all/page/"+str(page) #KP/JP
browser.get(url)
username = browser.find_element_by_xpath(
("/html/body/div[1]/div/form/div[2]/div/input"))
username.send_keys("billy123")
password = browser.find_element_by_xpath(
("/html/body/div[1]/div/form/div[3]/div/input"))
password.send_keys("gamecube123")
login_button = browser.find_element_by_xpath(
("/html/body/div[1]/div/form/div[4]/button"))
sleep(1)
login_button.click()

page = 2745 #FIRST PAGE
final_page = 3322 + 1 #FINAL PAGE
url = "http://kcnawatch.nknews.org/site/jp/all/page/"+str(page) #KP/JP
browser.get(url)
sleep(2)

article_count = 0 #ARTICLE COUNT
day_counter = 1 
last_day = "1" #START DAY
d = enchant.Dict("en_US")
english_flag = False
while page != final_page:
    for i in range(7,27):
        while True:
            try:
                date = browser.find_element_by_xpath(
                "/html/body/div[1]/div/div["+str(i)+"]/div/div[1]/div[2]/small")
                date = date.text.replace(",", "")
                date = date.split()
                month = date[0]
                day = date[1]
                year = date[2]
                if month == "January":
                    month = "01"
                if month == "February":
                    month = "02"
                if month == "March":
                    month = "03"
                if month == "April":
                    month = "04"
                if month == "May":
                    month = "05"
                if month == "June":
                    month = "06"
                if month == "July":
                    month = "07"
                if month == "August":
                    month = "08"
                if month == "September":
                    month = "09"
                if month == "October":
                    month = "10"
                if month == "November":
                    month = "11"
                if month == "December":
                    month = "12"
                if day != last_day:
                    day_counter = 1
                    last_day = day
                link = browser.find_element_by_xpath(
                    "/html/body/div[1]/div/div["+str(i)+"]/div/div[2]/div[1]/a")
                check = link.text.split()
                for word in check:
                    if d.check(word) == True:
                        english_flag = True
                        break
                if english_flag == True:
                    link.click()
                    if int(day) < 10:
                        ddd = "0" + day
                    else:
                        ddd = day
                    if day_counter < 10:
                        inc = "0" + str(day_counter)
                    else:
                        inc = str(day_counter)
                    file = (
                        open("/home/s/Project/Dissertation/"+
                            "2011/"+ #FOLDER NAME
                             year+"."+month+"."+ddd+"_"+inc+".txt", "w"))
                    title = browser.find_element_by_xpath(
                    "/html/body/div[1]/div/div[5]/div[1]/h2")
                    article = browser.find_element_by_xpath(
                    "/html/body/div[1]/div/div[5]/div[1]/article/p")
                    article_count += 1
                    file.write(title.text)
                    file.write("\n")
                    file.write(article.text)
                    file.write("\n")
                    file.close()
                    day_counter += 1
                    english_flag = False
                    sleep(randint(2,3))
                    browser.back()
            except Exception:
                print("error encountered at: " + str((time.time()-start_time)/60))
                print("current page is: " + str(page))
                print("continuing")
                pass        
            break        
    page += 1
    print(str(final_page-page) + " pages remaining")
    url = "http://kcnawatch.nknews.org/site/jp/all/page/"+str(page) #KP/JP
    browser.get(url)
    
browser.close()
print(str(article_count) + " articles scraped")
print("time:" + str((time.time()-start_time)/60))
