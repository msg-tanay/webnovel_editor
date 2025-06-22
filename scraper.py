from bs4 import BeautifulSoup
from selenium import webdriver

def scrape(link):
    result = []
    if "novelbin.com" in link:
        result.append("novelbin")

    elif "novelfull.com" in link:
        result.append("novelfull")
    
    else:
        raise ValueError("Unknown website")

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    driver.get(link)
    page_source = driver.page_source
    driver.quit()
    result.append(page_source)
    return result

def get_story(page_source):
    website = page_source[0]
    page_source = page_source[1]

    if website == "novelbin":
        start=page_source.find('<div></div>')+11
        s=page_source[start:]
        end=s.find('<div id="pf-1944-1">')
        soup = BeautifulSoup(s[:end], 'html.parser')
        for div in soup.find_all('div'):
            div.decompose()
        clean_text = soup.get_text()

    elif website == "novelfull":
        start = page_source.find("</iframe></div><p></p><p>")
        end = page_source.find('If you find any errors ( Ads popup,')
        s = page_source[start + 25 : end]
        soup = BeautifulSoup(s, 'html.parser')
        for div in soup.find_all('div'):
            div.decompose()
        clean_text = soup.get_text()

    else:
        raise ValueError(f"Unknown website: {website}")
    
    return clean_text

def find_next(page_source):
    website = page_source[0]
    page_source = page_source[1]

    if website == "novelbin":
        start=page_source.find('<a title')+8
        if start==-1:
            return False
        s=page_source[start:]
        end=s.find('class="btn btn-success')-2
        s=s[:end]
        start=s.find('href')+6
        return s[start:]
    
    elif website == "novelfull":
        soup = BeautifulSoup(page_source, "html.parser")
        links = soup.find_all("a", class_="btn btn-success")
        try:
            href = "https://novelfull.com" + links[3].get("href")
            print(f"Next chapter link: {href}")
            return href
        except:
            return False
    
    else:
        raise ValueError(f"Unknown website: {website}")

def save_pdf(link, output_filename = "story.pdf"):
    full_story = ""
    next_link = True
    while next_link:
        page_source = scrape(link)
        story = get_story(page_source)
        full_story = full_story + story + "\n\n\n\n"
        next_link = find_next(page_source)
        link = next_link
    print("All chapters scraped. Preparing PDF...")
    prepare_pdf(full_story, output_filename)

def prepare_pdf(full_story, output_filename):
    from fpdf import FPDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font('Helvetica', size=12)
    cleaned_story = full_story.encode("ascii", "ignore").decode("ascii")
    pdf.multi_cell(0, 10, cleaned_story)
    pdf.output(output_filename)

def add_chapter_to_pdf(chapter_text, pdf):
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font('Helvetica', size=12)
    cleaned_chapter = chapter_text.encode("ascii", "ignore").decode("ascii")
    pdf.multi_cell(0, 10, cleaned_chapter)

# def testing():
#     # link="https://novelbin.com/b/dragon-tamer/chapter-1-1-this-is-an-accident"
#     link = "https://novelfull.com/monarch-of-evernight/chapter-1-crimson-colored-night.html"
#     with open('story.txt','r') as f:
#         r=f.read()
#         next_link=find_next(r)
#     print(next_link)
# testing()