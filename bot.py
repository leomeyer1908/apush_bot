from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
from secrets import email, password

class Apush_Bot:
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=r"/usr/bin/chromedriver")

    def main(self):
        print("Logging in to Quizlet...")
        self.login()
        time.sleep(5)
        print("Getting term list...")
        term_list = self.getList()
        open("definitions.txt", "w").close() #this clears file
        d = open("definitions.txt", "a")
        for i in term_list:
            print("Finding definition for: " + i)
            definition = i + " - " + self.getDefinition(i) + "\n\n"
            d.write(definition)
            print(definition)
        d.close()

    def login(self):
        driver = self.driver
        driver.get("https://quizlet.com/")
        #click login button
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="SiteHeaderReactTarget"]/header/div[1]/div/div[2]/span[2]/div/div[3]/div/button[1]').click()
        #login with google
        time.sleep(4) #the 6 sometimes switches with 7
        try:
            driver.find_element_by_xpath('/html/body/div[6]/div/div[2]/div[1]/div[1]/div/a').click()
        except NoSuchElementException:
            driver.find_element_by_xpath('/html/body/div[7]/div/div[2]/div[1]/div[1]/div/a').click()
        #email
        time.sleep(2)
        email_bar = driver.find_element_by_xpath('//*[@id="identifierId"]')
        email_bar.send_keys(email)
        email_bar.send_keys(Keys.RETURN)
        #password
        time.sleep(2)
        pw_bar = driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
        pw_bar.send_keys(password)
        pw_bar.send_keys(Keys.RETURN)

    def getList(self):
        with open('words.txt') as rd:
            words = rd.read().split("\n")
        return words

    def getDefinition(self, term):
        driver = self.driver
        driver.get("https://www.google.com/")
        time.sleep(2)
        search_bar = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
        search_bar.send_keys(term + " quizlet" + " apush")
        search_bar.send_keys(Keys.RETURN)
        time.sleep(3)
        #click on first quizlet link
        try:
            driver.find_element_by_xpath('//*[@id="rso"]/div/div/div[1]/div/div/div[1]/a').click()
        except NoSuchElementException: #this is in case there is no first link
            driver.find_element_by_xpath('//*[@id="rso"]/div[2]/div/div/div/div[1]/a').click()
        #search for terms
        time.sleep(5)
        definit = self.find_term_num(term)
        try:
            print("try")
            return driver.find_element_by_xpath('//*[@id="SetPageTarget"]/div/div[3]/div[2]/div/div/section/div/section/div[' + self.find_term_num(term) + ']/div/div/div[1]/div/div[2]/div/a/span').text
        except NoSuchElementException:
            print("except")
            return driver.find_element_by_xpath('//*[@id="SetPageTarget"]/div/div[3]/div[2]/div/div/section/div/section/div[' + self.find_term_num(term) + ']/div/div/div[1]/div/div[2]/div/span/span').text
        except:
            return "N/A"
        #figure out how to get ctrl+f
        #send the 1st word of term, if no result, go to next word of term, if finishes with not result, go to 2nd link
        #go to the first find
        #return defintion of the found term

    def find_term_num(self, term):
        driver = self.driver
        #scrolls down a little to load some stuff
        driver.execute_script('window.scrollBy(0, 1000)')
        time.sleep(2)
        #gets string that says 'terms in this set (num)'
        try:
            str_with_num = driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[1]/div/div/div[3]/div[2]/div/div/section/div/div/h4/span/span').text
        except NoSuchElementException: #sometimes switches for some reason
            str_with_num = driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[1]/div/div/div[2]/div[2]/div/div/section/div/div/h4/span/span').text
        #takes the above str, cycles through every char, then checks if its a number, and then joins all nums together
        num = int(''.join([i for i in str_with_num if i.isdigit()]))
        term_wrd = term.split(' ')
        c_num = 0
        while c_num < num: #while instead of for so that it can add +1 to num in case of adds
            print(str(c_num+1) + "/" + str(num))
            try:
                try: #this is because the xpath sometimes changes for no reason
                    quizlet_term = driver.find_element_by_xpath('//*[@id="SetPageTarget"]/div/div[3]/div[2]/div/div/section/div/section/div[' + str(c_num+1) + ']/div/div/div[1]/div/div[2]/div/a/span').text
                except NoSuchElementException:
                    quizlet_term = driver.find_element_by_xpath('//*[@id="SetPageTarget"]/div/div[3]/div[2]/div/div/section/div/section/div[' + str(c_num+1) + ']/div/div/div[1]/div/div[2]/div/span/span').text
                #cycle through each word of term
                for j in term_wrd:
                    if j.lower() in quizlet_term.lower():
                        return str(c_num+1)
                c_num += 1
            except NoSuchElementException:
                c_num += 1
                num += 1
                # if c_num > 100:
                #     return "0"



#these are each of the terms on quizlet
#/html/body/div[3]/div[3]/div[1]/div/div/div[3]/div[2]/div/div/section/div/div[1]/h4/span/span
