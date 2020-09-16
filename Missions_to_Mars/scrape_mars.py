from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import re
import pandas as pd

def scrape():
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    slides = soup.find_all("li", {"class": "slide"})
    title = slides[0].find("div", {"class": "content_title"}).text
    pgraph = slides[0].find("div", {"class": "article_teaser_body"}).text

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    featured = soup.find_all("article", {"class": "carousel_item"})[0]["style"]
    featured_image_url = "https://www.jpl.nasa.gov" + re.search("\('([\w/\-\.]+)'\)", featured)[1]

    tables = pd.read_html(url)

    table_df = tables[0]
    html_table = table_df.to_html()

    hemisphere_dict = [{"title" : "Cerberus Hemisphere Enhanced", "img_url" : "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
                      {"title" : "Schiaparelli Hemisphere Enhance", "img_url" : "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
                      {"title" : "Syrtis Major Hemisphere Enhanced", "img_url" : "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"},
                      {"title" : "Valles Marineris Hemisphere Enhanced", "img_url" : "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"}]
    return {'title' : title, 'pgraph' : pgraph, 'img_url' : featured_image_url, 'table' : html_table, 'hemi_dict' : hemisphere_dict}