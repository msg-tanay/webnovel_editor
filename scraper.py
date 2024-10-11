from bs4 import BeautifulSoup
from selenium import webdriver

def scrape(link):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    driver.get(link)
    page_source = driver.page_source
    driver.quit()
    return page_source

def get_story(page_source):
    start=page_source.find('<div></div>')+11
    s=page_source[start:]
    end=s.find('<div id="pf-1944-1">')
    soup = BeautifulSoup(s[:end], 'html.parser')
    for div in soup.find_all('div'):
        div.decompose()
    clean_text = soup.get_text()
    return clean_text

def find_next(page_source):
    start=page_source.find('<a title')+8
    if start==-1:
        return -1
    s=page_source[start:]
    end=s.find('class="btn btn-success')-2
    s=s[:end]
    start=s.find('href')+6
    return s[start:]

# def testing():
#     # link="https://novelbin.com/b/dragon-tamer/chapter-1-1-this-is-an-accident"
#     with open('story.txt','r') as f:
#         r=f.read()
#         next_link=find_next(r)
#     print(next_link)
# testing()