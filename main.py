import time
import json
import random
import requests
import pandas as pd
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

headers4 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0',
    'Authorization': '', # Replace by your Bearer
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Referer': 'https://www.fotocasa.es'

  } 

def login_to_google(driver, google_email, google_password):  # Not entirely necessary but overall yields better results and won't be detected as often
    driver.get(f"https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fwww.google.com"
               f"%2F&ec=GAZAmgQ&hl=es&ifkv=ASKXGp04cdQ4ElNs3UzAFmWKdcPI7QaiJOFXmP5U0LuVchToD3rjr6lG7sQXY"
               f"Mvu-g8eGxD8CF4BpQ&passive=true&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S822338"
               f"424%3A1701230921611405&theme=glif")
    driver.maximize_window()

    time.sleep(random.uniform(1, 2))
    google_email_input = driver.find_element(By.ID, "identifierId")
    google_email_input.send_keys(google_email)
    time.sleep(random.uniform(1, 2))

    next_button = driver.find_element(By.ID, "identifierNext")
    next_button.click()

    time.sleep(random.uniform(2, 3))
    google_password_input = driver.find_element(By.XPATH,
                                                "/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[1]/div/form/span/section[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input")
    time.sleep(random.uniform(1, 2))
    google_password_input.send_keys(google_password)

    next_button2 = driver.find_element(By.ID, "passwordNext")
    next_button2.click()
    time.sleep(random.uniform(1, 2))


def get_json_response(url, page_number, capital):
    response = requests.get(url, headers=headers4)
    if response.status_code == 200:
        print("response status:", response.status_code)
        try:
            # Parse JSON response
            data = response.json()

            # Save the response to a file
            filename = f"page_{page_number}_{capital}.json"
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            return data
        except json.JSONDecodeError as e:
            print("Failed to decode JSON:", e)
            return None
    else:
        print("Failed to get data from URL:", url, "response status:", response.status_code)
        return None


def check_element_presence(driver, css_selector):
    try:
        driver.find_element(By.CSS_SELECTOR, css_selector)
        return True
    except NoSuchElementException:
        return False


def fotocasa(driver, page_number, sell_or_rent):
    ################
    capital = 'cadiz-capital'  ################## CHANGE EVERYTIME
    ############
    driver.get(f"https://www.fotocasa.es/es/{sell_or_rent}/viviendas/{capital}/todas-las-zonas/l/{page_number}?sortType=price&sortOrderDesc=false")
    time.sleep(random.uniform(3, 7))
    # html_text = driver.get_page_source()
    try:
        wait = WebDriverWait(driver, 4)
        agree_button = wait.until(EC.element_to_be_clickable((By.ID, 'didomi-notice-agree-button')))
        agree_button.click()
        time.sleep(random.uniform(1, 2))
    except (NoSuchElementException, TimeoutException):
        print("Agree button not found")

    ## While not mandatory I discovered that if their server detects js is executing inside your browser, it doesn't detect me as a bot and doesn't throw random captchas
    ## Simulates randomly scrolling down
    smooth_scroll_js = """    
                            let totalHeight = 0;
                            let distance = 100; // The number of pixels to scroll each step.
                            
                            function smoothScroll() {
                                let scrollHeight = document.body.scrollHeight;
                                window.scrollBy(0, distance);
                                totalHeight += distance;
                            
                                if (totalHeight >= scrollHeight) {
                                    return; // Stop scrolling
                                }
                            
                                let stepTime;
                                // Randomly decide to pause or scroll
                                if (Math.random() < 0.1) { // 10% chance to pause
                                    // Pause for a longer duration - between 500ms and 2000ms
                                    stepTime = Math.random() * 1500 + 500;
                                } else {
                                    // Normal scroll step time between 50ms and 150ms
                                    stepTime = Math.random() * 100 + 50;
                                }
                            
                                // Call smoothScroll again after the delay
                                setTimeout(smoothScroll, stepTime);
                            }
                            
                            // Start the first scroll
                            smoothScroll();
                        """

    driver.execute_script(smooth_scroll_js)
    time.sleep(random.uniform(31, 62))

    articles_data = []
    articles = driver.find_elements(By.TAG_NAME, 'article')
    for article in articles:
        article_info = {}
        href_element = article.find_element(By.XPATH, ".//a[@href]")
        article_info['Link'] = href_element.get_attribute("href")

        features = article.find_elements(By.CLASS_NAME, 're-CardFeatures-item')
        features_icon = article.find_elements(By.CLASS_NAME, 're-CardFeaturesWithIcons-feature')
        article_info['Features'] = ', '.join([feature.text for feature in features])
        article_info['Icon_Features'] = ', '.join([feature_icon.text for feature_icon in features_icon])

        articles_data.append(article_info)

    if check_element_presence(driver, '.re-SearchNoResults-title') is True:
        print("Last page reached.")
        return True, articles_data

    else:
        print("Last page not reached, continuing to next page.")
        return False, articles_data
      

  def main():
    driver = Driver(uc=True)
    login_to_google(driver, "your_mail@gmail.com", "your_password1234")
    all_articles_data = []
    page_number = 1  ## Set starting page, useful in case you want to resume from a certain point

    ## Manually setting the search area, the capital variable must match exactly how fotocasa names that region/area
    capital = 'cadiz'  ## Set to the city capital or to the zone/region defined in the URL
    # Example: with this URL https://www.fotocasa.es/es/comprar/viviendas/vitoria-gasteiz/todas-las-zonas/l
    # capital = 'vitoria-gasteiz'

    sell_or_rent = 'alquiler'  # 'alquiler' or 'comprar'   # 1 = comprar,     3 = alquiler
    if sell_or_rent == 'comprar':
        transaction_type_api = 1
    elif sell_or_rent == 'alquiler':
        transaction_type_api = 3
    else:
        print("Invalid input. Please enter 'comprar' or 'alquiler'.")
        exit(code=1)

    while True:
        print(f"Processing page {page_number}")
        last_page_reached, articles_data = fotocasa(driver, page_number, sell_or_rent)
        ########## CHANGE LOCATION COORDINATES FROM API REQUEST ##############
        ### Taken from the Network Tab, manually change the combinedLocationIds parameter and the latitude and longitude coordinates
        api_url =(f"https://web.gw.fotocasa.es/v2/propertysearch/search?combinedLocationIds=724,1,11,282,508,11012,0,0,0"  
                  f"&culture=es-ES&includePurchaseTypeFacets=true&isMap=false&isNewConstructionPromotions="
                  f"false&latitude=36.523&longitude=-6.28274&pageNumber={page_number}&platformId=1&propertyTypeId=2"
                  f"&sortOrderDesc=false&sortType=price&transactionTypeId={transaction_type_api}")

        get_json_response(api_url, page_number, capital)

        all_articles_data.extend(articles_data)
        if last_page_reached is True:
            break
        page_number += 1

    df = pd.DataFrame(all_articles_data)
    df.to_csv('articles_data.csv', index=False)
    driver.quit()


if __name__ == '__main__':
    main()


