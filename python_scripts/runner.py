from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys
import random
import requests
from bs4 import BeautifulSoup
from sklearn.externals import joblib
import datetime

def getQueriesFromFile(filename):
	with open(filename) as f:
		content = f.readlines()

	queries = [x.strip() for x in content]

	random.shuffle(queries)

	return queries

def googleSearch(webdriver, query):
	webdriver.get("http://google.com")
	searchBox = webdriver.find_element_by_name("q")
	searchBox.send_keys(query)
	searchBox.send_keys(Keys.ENTER)

def googleSearchAndClick(webdriver, query, bias='2', user):
	webdriver.get("http://google.com")
	searchBox = webdriver.find_element_by_name("q")
	searchBox.send_keys(query)
	searchBox.send_keys(Keys.ENTER)

	time.sleep(3)

	clf = joblib.load('bias_detector/political_bias_classifier_optimized.pkl')

	link = None
	url = None
	click_count = 0
	for i in range(1,6):

		try:
			xpath_link = "//*[@id='rso']/div[" + str(i) + "]/div/div/div/h3/a"
			xpath_url = "//*[@id='rso']/div[" + str(i) + "]/div/div/div/div/div/div[" + str(i) + "]/cite"
			link = webdriver.find_element_by_xpath(xpath_link)
			print("link: " + link.text)
			url = webdriver.find_element_by_xpath(xpath_url)
			print("url: " + url.text)
			print("--------------------------------")
		except:
			print("Didn't find link in first spot, trying again...")

		try:
			xpath_link = "//*[@id='rso']/div/div/div[" + str(i) + "]/div/div/h3/a"
			xpath_url = "//*[@id='rso']/div/div/div[" + str(i) + "]/div/div/div/div/div/cite"
			link = webdriver.find_element_by_xpath(xpath_link)
			print("link: " + link.text)
			url = webdriver.find_element_by_xpath(xpath_url)
			print("url: " + url.text)
			print("--------------------------------")
		except:
			print("didn't find link in second spot, skipping...")
			print("--------------------------------")
			continue

		try:
			#if user is control, click the link, otherwise classify
			if bias is '2':
				ActionChains(webdriver).move_to_element(link).click().perform()
				print("clicked")
				click_count += 1
				time.sleep(2)
				webdriver.back()
				time.sleep(2)
			else:
				#download the page
				page = requests.get(url.text)
				print("getting url: " + url.text)
				#use BeautifulSoup to parse the html content of the page and extract the text
				soup = BeautifulSoup(page.content, 'html.parser')
				text = "".join([p.text for p in soup.find_all("p")])
				prediction = clf.predict([text])
				print("prediction: " + prediction)
				#check to see if the bias of the link matches the user's bias
				#1 is conservative, 0 is liberal
				if bias == prediction:
					ActionChains(webdriver).move_to_element(link).click().perform()
					print("clicked")
					click_count += 1
					time.sleep(2)
					webdriver.back()
					time.sleep(2)
				else:
					print("incorrect bias, not clicking link")

			print("--------------------------------")
		except:
			print("error: " + str(sys.exc_info()[0]))
			print("--------------------------------")
	with open("log.txt", "a") as logfile:
		date = str(datetime.date.today())
		logfile.write("{0}\t{1}\t{2}\t{3}\n".format(date, user, bias, click_count)
)




def login(webdriver, email, password):
	webdriver.get("http://google.com")
	sign_in_button = webdriver.find_element_by_id("gb_70")
	sign_in_button.click()

	email_field = webdriver.find_element_by_id("identifierId")
	email_field.send_keys(email)
	email_field.send_keys(Keys.ENTER)

	time.sleep(5)
	password_field = webdriver.find_element_by_name("password")
	time.sleep(5)
	password_field.send_keys(password)
	password_field.send_keys(Keys.ENTER)
	time.sleep(5)

def without_click_test():
	#array of tuples (username, password, queryset, bias)
	users = []
	users.append(("joes9358", "controluser", "queries_controversial.txt", "2"))
	users.append(("janetheplummer123", "controltwo", "queries_controversial.txt", "2"))
	users.append(("js4425947", "liberaluser", "queries_liberal.txt", "0"))
	users.append(("jplum713", "conservativeuser", "queries_conservative.txt", "1"))

	for u in users:
		queries = getQueriesFromFile("queries/" + u[2])
		driver = webdriver.Firefox()

		login(driver, u[0], u[1])
		for q in queries:
			googleSearch(driver, q)
			time.sleep(5)

		driver.quit()
		time.sleep(5)

	driver.quit()

def with_click_test():
	#array of tuples (username, password, queryset, bias)
	users = []

	users.append(("moreese978", "controlclick", "queries_controversial.txt", "2"))
	users.append(("emzhou01", "controlclicktwo", "queries_controversial.txt", "2"))
	users.append(("lastova2017", "liberalclicker", "queries_liberal.txt", "0"))
	users.append(("wg68309", "conservativeclicker", "queries_conservative.txt", "1"))

	for u in users:
		queries = getQueriesFromFile("queries/" + u[2])
		driver = webdriver.Firefox()

		login(driver, u[0], u[1])
		for q in queries:
			googleSearchAndClick(driver, q, u[3], u[1])
			time.sleep(5)

		driver.quit()
		time.sleep(5)

	driver.quit()

if __name__ == '__main__':
	#without_click_test()
	with_click_test()
