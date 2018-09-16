from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)
    
def scrape():
    
    browser = init_browser()
    
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)   
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    featured_image_url_raw = soup.find("article", class_="carousel_item")["style"][23:75]
    featured_image_url = "https://www.jpl.nasa.gov"  + featured_image_url_raw 

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    url = 'http://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['Description', 'Values']
    df = df.set_index('Description')
    html_table = df.to_html()
    html_table = html_table.replace('\n', '')

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all("div", class_="description")
    hemisphere_image_urls = []

    for result in results:
        dic = {}
        
        browser = webdriver.Chrome("C:/Users/alexb/LearnPython/web_scraping/chromedriver.exe")
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.get(url)
        
        click = result.h3.text
        browser.find_element_by_link_text(click).click()
        soup_level2=BeautifulSoup(browser.page_source, 'lxml')
        img_url = soup_level2.find("div", class_="downloads").a["href"]
        title = soup_level2.find("h2", class_="title").text
        title = title.split(" ")
        title = title[:-1]
        title = ' '.join(title)
        
        dic['title'] = title
        dic['img_url'] = img_url
        hemisphere_image_urls.append(dic)

    mars_dic = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "html_table": html_table,
        "mars_facts": hemisphere_image_urls

    }

    return mars_dic    
    
    
    