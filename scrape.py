# import threading;
import requests;
import time;
from bs4 import BeautifulSoup
from pytimedinput import timedKey

list_url_format = 'https://phishtank.org/phish_search.php?page=@page@&valid=n&Search=Search'
detail_url_format = 'https://phishtank.org/phish_detail.php?phish_id=@id@'
exported_ids_file = 'phishtank_ids.csv'
exported_urls_file = 'phishtank_urls.csv'
n = 10000
scraped = 0
urls = 0
threads = []

# clear file
open(exported_ids_file, 'w').close()
open(exported_urls_file, 'w').close()

def fetch_and_wait(url):
    html = requests.get(url).text
    rate_limited = html.find('You have exceeded the number of allowed requests. Please try again shortly.') != -1
    while (rate_limited):
        time.sleep(10)
        html = requests.get(url).text
        rate_limited = html.find('You have exceeded the number of allowed requests. Please try again shortly.') != -1
    return html


def get_list_url(page):
    return list_url_format.replace('@page@', str(page))

def get_detail_url(id):
    return detail_url_format.replace('@id@', str(id))

def scrape(page):
    global scraped
    global urls
    list_html = fetch_and_wait(get_list_url(page))
    list_soup = BeautifulSoup(list_html, 'html.parser')
    table = list_soup.find('table', {'class': 'data'})
    rows = table.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if len(cells) == 0:
            continue
        phish_id = cells[0].contents[0].text
        with open(exported_ids_file, 'a') as id_f:
            id_f.write(phish_id + '\n')
        detail_html = fetch_and_wait(get_detail_url(phish_id))
        detail_soup = BeautifulSoup(detail_html, 'html.parser')
        spans = detail_soup.find_all('span')
        if len(spans) < 3:
            print(f'No URL found for id {phish_id}. See "html/{phish_id}.html".')
            with open(f'failed_htmls/{phish_id}.html', 'w') as f:
                f.write(detail_html)
            continue

        urls += 1
        url = spans[2].contents[0].text
        with open(exported_urls_file, 'a') as url_f:
            url_f.write(url + '\n')
        print(f'Scraped page {page}. Total URLs collected: {urls}')
    
    scraped += 1

def scrape_pages(pages):
    for page in range(1, pages):
        scrape(page)
        # t = threading.Thread(target=scrape, args=(page,))
        # t.start()
        # timedOut, _ = timedKey("Queued page " + str(page) + ". Press any key to exit...\n", 5)
        # if not timedOut:
        #     print("Exiting...")
        #     break

def scrape_indefinitely():
    page = 1
    while True:
        scrape(page)
        page += 1

print(f'Scraping {n} pages...')
scrape_pages(n);

# wait for all threads to finish
for t in threads:
    t.join()