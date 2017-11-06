from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random

def getQueriesFromFile(filename):
	with open(filename) as f:
		content = f.readlines()

	queries = [x.strip() for x in content]

	random.shuffle(queries)

	return queries

def googleSearch(webdriver, query):
	webdriver.get("http://google.com")
	searchBox = webdriver.find_element_by_name("q"); 
	searchBox.send_keys(query)
	searchBox.send_keys(Keys.ENTER)

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
	users.append("joes9358", "controluser", "neutral.txt")
	users.append(("janetheplummer123", "controltwo", "neutral.txt"))
	users.append("js4425947", "liberaluser", "liberal.txt")
	users.append("jplum713", "conservativeuser", "conservative.txt")

	for u in users:
		queries = getQueriesFromFile("queries/" + u[2])
		driver = webdriver.Firefox()

		login(driver, u[0], u[1])
		for q in queries:
			googleSearch(driver, q)
			time.sleep(5)

		driver.Quit()

if __name__ == '__main__':
	main()