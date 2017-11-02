package main;

import java.io.FileReader;
import java.util.*;
import java.util.concurrent.TimeUnit;

import org.openqa.selenium.By;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

public class Main {

	public static void main(String[] args) {
		
		String [] liberalQueries = getQueriesFromFile("./liberalQueries");
		String [] conservativeQueries = getQueriesFromFile("./conservativeQueries");
		
		//instantiate Selenium's Chrome WebDriver
		System.setProperty("webdriver.chrome.driver", "./chromedriver");
		ChromeDriver driver = new ChromeDriver();
		driver.manage().window().maximize();
		
		for(String query : liberalQueries) {
			System.out.println(query);
			googleSearch(driver, query);
//			bingSearch(driver, query);

		}
		
		for(String query : conservativeQueries) {
			System.out.println(query);
			googleSearch(driver, query);
//			bingSearch(driver, query);
		}
		
		driver.quit();
	}
	
	public static String [] getQueriesFromFile(String filepath) {
		String s = "";
		try {
			Scanner file = new Scanner(new FileReader(filepath));
			while(file.hasNextLine()) {
			    s = s + "," + file.nextLine();
			}
			file.close();
		}catch(Exception e) {
			e.printStackTrace();
		}
		
		return s.split(",");
	}
	
	public static void googleSearch(WebDriver driver, String query) {
		try{
			driver.get("https://www.google.com"); //go to google.com
			
			//Selenium is erroring out when trying to click on first document after searching. WebDriverWait supposedly waits until the element is visible/click-able, 
			//but was still causing problems last time I checked
			WebDriverWait wait = new WebDriverWait(driver, 20);
			
			wait.until(ExpectedConditions.presenceOfElementLocated(By.name("q")));
			WebElement searchBox = driver.findElement(By.name("q")); //fill search field with query
			searchBox.sendKeys(query);
			searchBox.sendKeys(Keys.RETURN); // instead of finding a button, just hit enter. Was causing errors because original button was hidden by autocomplete suggestions
			
			//XPATHs for first returned document and corresponding URL (not image, map, or ad. just link of first rank). 
			//It is consistent because @id='rso' differentiates it from the other types of non-relevant documents
			String docXPath = "//*[@id=\"rso\"]/div[2]/div/div[1]/div/div/h3/a";
			String urlXPath = "//*[@id=\"rso\"]/div[2]/div/div[1]/div/div/div/div/div[1]/cite";

//			wait.until(ExpectedConditions.presenceOfElementLocated(By.xpath(docXPath)));
//			WebElement firstDocument = driver.findElement(By.xpath(docXPath));
//			String documentUrl = driver.findElement(By.xpath(urlXPath)).getText();
//			System.out.println(documentUrl);
//			firstDocument.click();
		}catch(Exception e) {
			System.out.println("Error searching query in Google: " + query);
			e.printStackTrace(); //if there is an error, print the stack trace and close chrome
//			driver.quit();
		}
	}
	
	public static void bingSearch(WebDriver driver, String query) {
		try{
			driver.get("https://www.bing.com"); //go to bing.com
			
			WebElement searchBox = driver.findElement(By.name("q")); //fill search field with query
			searchBox.sendKeys(query);
			
			WebElement searchButton = driver.findElement(By.name("go")); //click search
			searchButton.click();
			
		}catch(Exception e) {
			System.out.println("Error searching query in Bing: " + query);
			e.printStackTrace(); //if there is an error, print the stack trace and close chrome
			driver.quit();
		}
	}
}
