from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

def scrape_quotes(url, file_path):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Use WebDriver Manager to handle ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            while True:
                driver.get(url)
                
                # Wait until quotes are loaded
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'quote'))
                )

                # Get page source and parse with BeautifulSoup
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')

                # Extract quotes data
                quotes = soup.find_all('div', class_='quote')

                for quote in quotes:
                    text = quote.find('span', class_='text').text
                    author = quote.find('small', class_='author').text
                    tags = [tag.text for tag in quote.find_all('a', class_='tag')]
                    
                    file.write(f"Quote: {text}\n")
                    file.write(f"Author: {author}\n")
                    file.write(f"Tags: {', '.join(tags)}\n")
                    file.write("-" * 40 + "\n")

                try:
                    # Pagination: Go to next page
                    next_button = driver.find_element(By.CSS_SELECTOR, 'li.next > a')
                    if next_button:
                        next_page_url = next_button.get_attribute('href')
                        print(f"Next page URL: {next_page_url}")
                        url = next_page_url  # Update URL to next page
                    else:
                        print("No more pages.")
                        break  # Exit loop if no more pages
                except Exception as e:
                    print(f"No more pages or error: {e}")
                    break  # Exit loop if no more pages or an error occurs

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    url = 'http://quotes.toscrape.com'
    file_path = 'quotes.txt'
    scrape_quotes(url, file_path)
