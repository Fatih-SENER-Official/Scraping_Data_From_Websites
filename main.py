from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up WebDriver options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless if you don't need a browser UI

# Set up the WebDriver (adjust the path to your chromedriver)
service = Service(executable_path="/path/to/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to the e-commerce site
url = "https://www.amazon.com/s?k=laptop"
driver.get(url)

# Wait for elements to load
wait = WebDriverWait(driver, 10)

while True:
    # Extract product titles
    titles = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "//span[@class='a-size-medium a-color-base a-text-normal']")))

    # Extract product prices
    prices = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[@class='a-price-whole']")))

    # Extract product ratings
    ratings = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[@class='a-icon-alt']")))

    # Print out the extracted data
    for title, price, rating in zip(titles, prices, ratings):
        print(f"Title: {title.text}, Price: {price.text}, Rating: {rating.text}")

    # Check if a "Next" button exists and click it
    try:
        next_button = driver.find_element(By.XPATH, "//a[@class='s-pagination-next']")
        next_button.click()
        WebDriverWait(driver, 10).until(EC.staleness_of(next_button))  # Wait for the page to load
    except:
        break  # No more pages, exit the loop

# Close the browser
driver.quit()