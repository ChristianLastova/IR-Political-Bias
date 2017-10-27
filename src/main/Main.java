package main;

import java.io.FileReader;
import java.util.*;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;

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
//			googleSearch(driver, query);
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
			
			WebElement searchBox = driver.findElement(By.name("q")); //fill search field with query
			searchBox.sendKeys(query);
			//*[@id="rso"]/div[2]/div/div[1]/div/div/h3/a
			
			WebElement searchButton = driver.findElement(By.name("btnK")); //click search
			searchButton.click();
		}catch(Exception e) {
			System.out.println("Error searching query in Google: " + query);
			e.printStackTrace(); //if there is an error, print the stack trace and close chrome
			driver.quit();
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
