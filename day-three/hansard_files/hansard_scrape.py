import requests
import bs4
import random
import time

test_url = "https://www.parliament.nz/en/pb/hansard-debates/rhr/combined/HansD_20250313_20250313"
test_headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0'}

parliament_url = "https://www.parliament.nz"
hansard_link_html = "https://www.parliament.nz/en/pb/hansard-debates/rhr/"

def scrape_hansard_links(page_link, parliament_url, headers):
        hansard_links = [] 
        time.sleep(1+random.random())
        current_url = parliament_url+page_link
        raw_page = requests.get(current_url, headers=headers)
        page_html = bs4.BeautifulSoup(raw_page.content)
        hansard_headings = page_html.find_all("h2", {"class": "hansard__heading"})
        
        for hansard in hansard_headings:
            hansard_links.append(parliament_url+hansard.findChild('a', recursive=False)["href"])
        return hansard_links

def get_hansard_links(hansard_url, parliament_url, headers):
    hansard_links = []
    first_page = requests.get(hansard_url, headers=headers)
    first_soup = bs4.BeautifulSoup(first_page.content)
    page_list = first_soup.find_all('a', {'class':'theme__link js-pagination-link'})
    page_links = []

    for link in page_list:
        href_pointer = link["href"]
        if not href_pointer in page_links:
            page_links.append(href_pointer)

    hansard_headings = first_soup.find_all("h2", {"class": "hansard__heading"})
    for hansard in hansard_headings:
        hansard_links.append(parliament_url+hansard.findChild('a', recursive=False)["href"])
    
    while page_links:
         hansard_links += scrape_hansard_links(page_links.pop(), parliament_url, headers)
    return hansard_links

def save_html(html, save_file):
    with open(save_file, "w") as f:
        f.write(str(html))

def scrape_hansard(url, headers):
    html_raw = requests.get(url, headers=headers)
    html_soup = bs4.BeautifulSoup(html_raw.content)
    hansard_tab = html_soup.find_all('div', {'class': 'section'})
    return hansard_tab

hansard_links = get_hansard_links(hansard_link_html, parliament_url, test_headers)

big_html_str = ""
for link in hansard_links:
    big_html_str+=str(scrape_hansard(link, test_headers))
save_html(big_html_str, "hansard_scraping.html")