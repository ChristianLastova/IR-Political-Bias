from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import requests
from bs4 import BeautifulSoup
from sklearn.externals import joblib

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

def googleSearchAndClick(webdriver, query):
	webdriver.get("http://google.com")
	searchBox = webdriver.find_element_by_name("q")
	searchBox.send_keys(query)
	searchBox.send_keys(Keys.ENTER)

	time.sleep(3)

	clf = joblib.load('bias_detector/political_bias_classifier_optimized.pkl')

	try:
		link = webdriver.find_element_by_xpath("//*[@id='rso']/div[1]/div/div/div/h3/a")
		print("link: " + link.text)
		url = webdriver.find_element_by_xpath("//*[@id='rso']/div[1]/div/div/div/div/div/div[1]/cite")
		print("url: " + url.text)
		ActionChains(webdriver).move_to_element(link).click().perform()
		#download the page
		page = requests.get(url.text)
		#use BeautifulSoup to parse the html content of the page and extract the text
		soup = BeautifulSoup(page.content, 'html.parser')
		text = soup.get_text()
		clf.predict([text])
		print("--------------------------------")
	except:
		try:
			link = webdriver.find_element_by_xpath("//*[@id='rso']/div/div/div[1]/div/div/h3/a")
			print("link: " + link.text)
			url = webdriver.find_element_by_xpath("//*[@id='rso']/div/div/div[1]/div/div/div/div/div/cite")
			print("url: " + url.text)
			ActionChains(webdriver).move_to_element(link).click().perform()
			time.sleep(3)
			print("--------------------------------")
		except:
			print("didn't find link")
		

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



def main():

	#array of tuples (username, password, queryset)
	users = []
	#users.append(("joes9358", "controluser", "queries_controversial.txt"))
	#users.append(("janetheplummer123", "controltwo", "queries_controversial.txt"))
	#users.append(("js4425947", "liberaluser", "queries_liberal.txt"))
	#users.append(("jplum713", "conservativeuser", "queries_conservative.txt"))

	users.append(("moreese978", "controlclick", "queries_controversial.txt"))

	for u in users:
		queries = getQueriesFromFile("queries/" + u[2])
		driver = webdriver.Firefox()

		login(driver, u[0], u[1])
		for q in queries:
			googleSearchAndClick(driver, q)
			time.sleep(5)

		driver.quit()
		time.sleep(5)

	driver.quit()

if __name__ == '__main__':
	main()