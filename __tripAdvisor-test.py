import sys
import os
from datetime import datetime
import pandas as pd
import time
from time import localtime, strftime
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
# from pandas import DataFrame
from bs4 import BeautifulSoup

# Global variables
column_titles = ['Title', 'Rating', 'Review Count', 'User Reviews', 'Phone Number', 'Address', 'Locality', 'Country', 'Date Generated']  # , 'Opening Hours']
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}


def search(query):
    # Set up browser
    chrome_options = Options()
    # chrome_options.add_argument("--enable-fast-unload")
    browser = webdriver.Chrome(chrome_options=chrome_options)
    # Navigate to trip tripadvisor
    main_url = 'https://www.tripadvisor.com/Attractions'
    site_url = "https://www.tripadvisor.com"
    # Should redirect to the correct local domain as needed (ex- .sg) AFAIK
    browser.get(main_url)

    # Search for the place provided and click on the "Things to Do" searchbar
    wait = WebDriverWait(browser, 1)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "typeahead_input")))
    searchbar = browser.find_element_by_class_name("typeahead_input")
    searchbar.send_keys(query)
    # searchbar.send_keys(Keys.RETURN)
    browser.find_element_by_id("SUBMIT_THINGS_TO_DO").click()

    # Wait for page load
    try:
        wait = WebDriverWait(browser, 1)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "listing_title")))
    except TimeoutException:
        time.sleep(1)

    # Visit all pages
    page_num = 0
    try:
        total_pages = browser.find_element_by_xpath("""//*[@id="FILTERED_LIST"]/div[34]/div/div/div/a[6]""")
        pages_to_scrape = int(total_pages.text)
        pages_to_scrape //= 3
    except Exception:
        pages_to_scrape = 1

    data = []
    date_gen = datetime.today().replace(microsecond=0)

    while page_num < pages_to_scrape:
        page_num += 1

        # Get each attraction
        soup = BeautifulSoup(browser.page_source, "html5lib")
        attractions = soup.find_all("div", {"class": "listing_title "})
        links = [site_url + item.a['href'] for item in attractions if "Attraction_Review" in item.a['href']]
        numlinks = len(links)
        print(f"\nFound {numlinks} links on page {page_num}/{pages_to_scrape}--", end="")

        try:
            next_page = site_url + soup.find("a", class_="next").get('href')
        except AttributeError:
            next_page = None

        for i in range(numlinks):
            print()
            # print(str(i) + ".", end="", flush=True)
            # Visit each page
            browser.get(links[i])

            # Scrape data
            soup = BeautifulSoup(browser.page_source, 'html5lib')
            try:
                title = soup.find('h1', id='HEADING').text
            except Exception:
                title = None
            try:
                review_count = soup.find('span', class_='reviews_header_count').text.strip('()')
            except Exception:
                review_count = None
            try:
                rating = soup.find("span", class_="overallRating").text
            except Exception:
                rating = None
            try:
                phone = soup.find("div", class_=['phone']).text
                for c in phone:
                    if c.isalpha():
                        phone = None
                        break
            except Exception:
                phone = None
            try:
                address = soup.find("span", class_="street-address").text.rstrip(',')
            except Exception:
                address = None
            try:
                exaddress = soup.find("span", class_="extended-address").text
            except Exception:
                exaddress = None
            try:
                local = soup.find("span", class_="locality").text.replace(',', '')
            except Exception:
                local = None
            try:
                country = soup.find("span", class_="country-name").text
            except Exception:
                country = None
            try:

                user_review_list = soup.find_all("div", class_="ppr_rup ppr_priv_location_reviews_list_resp")
                print(f"On page {i} we found {len(user_review_list)} reviews of {title}", end="")
                user_reviews = {ur.find("div", class_="info_text").div.text: ur.find("p", class_="partial_entry").text for ur in user_review_list}
            except Exception as e:
                print(e)
                user_reviews = None

            if address is None:
                address = exaddress

            newrow = [title, rating, review_count, user_reviews, phone, address, local, country, date_gen]
            data.append(newrow)

        if next_page:
            browser.get(next_page)
        else:
            print("No more pages")
            break

    browser.quit()
    final_df = pd.DataFrame(data, columns=list(column_titles))
    return final_df


def main():
    start = time.perf_counter()
    print(strftime("Starting at %H:%M:%S", localtime()))
    if len(sys.argv) < 2:
        destinations = ['Bali', 'Manila', 'malaysia']
    else:
        destinations = sys.argv[1:]

    try:
        savefolder = "data"
        os.mkdir(savefolder)
    except Exception as e:
        pass

    print("Searching:", end="")
    [print(" " + p.capitalize(), end="") for p in destinations]
    print()

    for place in destinations:
        place = place.capitalize()
        # os.chdir(savefolder)
        os.path.join(os.getcwd(), "data")
        filepath = os.path.join(os.path.abspath(savefolder), place + "_data.csv")
        print("Beginning search in", place)
        df = search(place)
        df.to_csv(path_or_buf=filepath, index_label="Index", columns=column_titles)
        print(strftime("\nFinished at %H:%M:%S\n", localtime()))
        print(df.head())
    finish = time.perf_counter()
    execution_time = (finish - start) / 60
    print("Program took {:.2f} minutes to complete".format(execution_time))


if __name__ == '__main__':
    main()
