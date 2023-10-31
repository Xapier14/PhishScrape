import glob
from bs4 import BeautifulSoup

def test_soup():
    # for each html file in html/
    htmls = glob.glob('failed_htmls/*.html')

    for html in htmls:
        with open(html, 'r') as f:
            soup = BeautifulSoup(f.read(), 'lxml')
            # all spans
            spans = soup.find_all('span')
            if len(spans) == 0:
                print(f'No URL found for {html}.')
                continue
            url = spans[2].contents[0].text
            print(url)

if __name__ == '__main__':
    test_soup()