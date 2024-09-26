# have to add date, fix country, title, review link, have to check without sign in, create amazon acc for this, 
# check if signin url can be constructed dynamically, add time taken 



import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import re
from datetime import datetime

service = Service('/Users/shiv/nii/selenium/chromedriver')  
driver = webdriver.Chrome(service=service)

marketplace_signin_urls = {
    "amazon.co.uk": "https://www.amazon.co.uk/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.co.uk%2F%3Fref_%3Dnav_custrec_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=gbflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0",
    "amazon.fr": "https://www.amazon.fr/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.fr%2F%3Fref_%3Dnav_custrec_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=frflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0",
    "amazon.de": "https://www.amazon.de/-/en/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.de%2F%3F_encoding%3DUTF8%26ref_%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=deflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0",
    "amazon.es": "https://www.amazon.es/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.es%2F%3Fref_%3Dnav_custrec_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=esflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0",
    "amazon.it": "https://www.amazon.it/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.it%2F%3Fref_%3Dnav_custrec_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=itflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0",
    "amazon.se": "https://www.amazon.se/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.se%2Fgp%2Fcss%2Fhomepage.html%2Fref%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=seflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0",
    "amazon.com.br": "https://www.amazon.com.br/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com.br%2F%3Fref_%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=brflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0",
    "amazon.ca": "https://www.amazon.ca/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.ca%2F%3Fref_%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=caflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0",
    "amazon.in": "https://www.amazon.in/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.in%2F%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=inflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0",
    "amazon.com": "https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_custrec_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0",
}

def get_marketplace_and_signin_url(url):
    for key in marketplace_signin_urls:
        if key in url:
            return key, marketplace_signin_urls[key]
    return None, None

def amazon_login(email, password, signin_url):
    driver.get(signin_url)
    
    try:
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'ap_email'))
        )
        email_field.send_keys(email)
        
        driver.find_element(By.ID, 'continue').click()

        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'ap_password'))
        )
        password_field.send_keys(password)
        driver.find_element(By.ID, 'signInSubmit').click()

        # Waiting for login to complete 
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, 'nav-link-accountList'))
        )
    except Exception as e:
        print(f"Login failed: {e}")
        driver.quit()
        raise

import os

def parse_reviews(product_info, output_csv_path):
    reviews_data = []
    asin = product_info['ASIN/REF']  
    marketplace, signin_url = get_marketplace_and_signin_url(product_info['URL']) 
    
    if not marketplace:
        print(f"Unknown marketplace for URL: {product_info['URL']}")
        return
    
    url = f"https://{marketplace}/product-reviews/{asin}"
    
    # scraping starts
    while url:
        try:
            driver.get(url)
            time.sleep(5)  # Wait for the page to load

            html_data = BeautifulSoup(driver.page_source, 'html.parser')
            review_elements = html_data.find_all('div', {'data-hook': 'review'})

            for review_element in review_elements:
                text_parts = review_element.find_all('a', {'data-hook': 'format-strip'})
                text = " | ".join([part.get_text() for part in text_parts if part is not None])

                size = "Not available"
                pattern_name = "Not available"
                style = "Not available"

                size_pattern = r"Size:\s*([^|]+)"
                pattern_name_pattern = r"Pattern Name:\s*([^|]+)"
                style_pattern = r"Style:\s*([^|]+)"

                size_match = re.search(size_pattern, text)
                pattern_name_match = re.search(pattern_name_pattern, text)
                style_match = re.search(style_pattern, text)

                if size_match:
                    size = size_match.group(1).strip()
                if pattern_name_match:
                    pattern_name = pattern_name_match.group(1).strip()
                if style_match:
                    style = style_match.group(1).strip()

                review_date_text = review_element.find('span', {'data-hook': 'review-date'})
                review_date_text = review_date_text.get_text() if review_date_text else 'N/A'

                rating = review_element.select_one('*[data-hook*="review-star-rating"]')

                review_date = 'N/A'
                country = 'N/A'
                if review_date_text:
                    date_parts = review_date_text.strip().split(' on ')
                    if len(date_parts) > 1:
                        try:
                            review_date = datetime.strptime(date_parts[-1], '%d %B %Y').strftime("%d/%m/%Y")
                        except ValueError:
                            review_date = 'N/A'
                    if 'Reviewed in ' in review_date_text:
                        country = review_date_text.strip().split('Reviewed in ')[1].split(' on ')[0]

                reviews_data.append({
                    "Marketplace": marketplace,
                    "ASIN": asin,
                    "Product URL": url,
                    "Unique Review ID": review_element.get('id'),
                    "Unique Review URL": f"https://{marketplace}" + '/gp/customer-reviews/' +review_element.get('id'),
                    "Name of User": review_element.find('span', {'class': 'a-profile-name'}).get_text() if review_element.find('span', {'class': 'a-profile-name'}) else "N/A",
                    "Location and Date": review_date_text,
                    "Country": country,
                    "Rating": re.search(r"(\d+\.*\d*) out", rating.get_text()).group(1) if rating else 'N/A',
                    "Description": "".join([part.get_text() for part in review_element.find_all('span', {'data-hook': 'review-body'})]).strip() if review_element.find_all('span', {'data-hook': 'review-body'}) else 'N/A',
                    "Size": size,
                    "Pattern_Name": pattern_name,
                    "Style": style,
                    "Verified Purchase": bool(review_element.find('span', {'data-hook': 'avp-badge'})),
                    "Helpful Votes": review_element.find('span', {'data-hook': 'helpful-vote-statement'}).get_text() if review_element.find('span', {'data-hook': 'helpful-vote-statement'}) else 'N/A',
                    "Model Number": product_info['Model Number'],
                    "Part Number": product_info['Part Number'],
                    "SKU": product_info['SKU'],
                    "Brand": product_info['Brand']
                })
            
            next_page = html_data.find('li', {'class': 'a-last'})
            if next_page and next_page.find('a'):
                url = 'https://' + marketplace + next_page.find('a').get('href')
            else:
                url = None

            print(f"Fetching reviews from: {url}")

        except Exception as e:
            print(f"An error occurred: {e}")
            break

    data = pd.DataFrame(reviews_data)
    if os.path.exists(output_csv_path):
        data.to_csv(output_csv_path, mode='a', header=False, index=False)
    else:
        data.to_csv(output_csv_path, index=False)


def main():
    input_csv_path = '/Users/shiv/nii/selenium/Book2.csv'  
    output_csv_path = '/Users/shiv/nii/selenium/product_reviews.csv'  
    
    email = input("Please enter your E-mail: ") 
    password = input("Please enter your password: ")  

    products_df = pd.read_csv(input_csv_path)
    
    first_url = products_df['URL'].iloc[0]
    _, signin_url = get_marketplace_and_signin_url(first_url)
    if signin_url:
        amazon_login(email, password, signin_url)
    else:
        print("Unable to determine sign-in URL based on the provided URLs.")
        return
    
    # Iterate over each product and parse reviews
    for _, product_info in products_df.iterrows():
        print(f"Scraping reviews for ASIN {product_info['ASIN/REF']}")
        parse_reviews(product_info, output_csv_path)
    
    driver.quit()


if __name__ == "__main__":
    main()