from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def getQueriesFromFile(filename):
	with open(filename) as f:
		content = f.readlines()

	queries = [x.strip() for x in content]

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
	queries = getQueriesFromFile("queries/liberal.txt")

	driver = webdriver.Firefox()

	login(driver, "janetheplummer123", "controltwo")
	for q in queries:
		googleSearch(driver, q)

if __name__ == '__main__':
	main()