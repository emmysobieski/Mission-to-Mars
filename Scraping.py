# Import Splinter, BeautifulSoup and Pandas
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    # Set News Title and Paragraph Variables
    news_title, news_paragraph = mars_news(browser)

    #Set URL and titles
    hemisphere_urls_list = fetch_mars_hemisphere_url(browser)
    
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        
        "cerberus_title": hemisphere_urls_list[0][0],
        "cerberus_urls": hemisphere_urls_list[0][1],
        "cerberus_thumbnail_urls": hemisphere_urls_list[0][2],
        
        "schiaparelli_title": hemisphere_urls_list[1][0],
        "schiaparelli_urls": hemisphere_urls_list[1][1],
        "schiaparelli_thumbnail_urls": hemisphere_urls_list[1][2],
        
        "syrtis_major_title": hemisphere_urls_list[2][0],
        "syrtis_major_urls": hemisphere_urls_list[2][1],
        "syrtis_major_thumbnail_urls": hemisphere_urls_list[2][2],
        
        "valles_marineris_title": hemisphere_urls_list[3][0],
        "valles_marineris_urls": hemisphere_urls_list[3][1],
        "valles_marineris_thumbnail_urls": hemisphere_urls_list[3][2]
        
    }
    
    browser.quit()
    return data

# Set up path and initiate chromebrowser in splinter
executable_path = {'executable_path': 'C:/Users/esobieski/Documents/Berkeley/Mission-to-Mars/chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

# Mars News Function
def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to soup object, then quit the browser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    # Add try/except for error handling
    try: 
        slide_elem = news_soup.select_one('ul.item_list li.slide')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    return news_title, news_p
    
    
# Fetch URLs of Mars hemispheres
def fetch_mars_hemisphere_url(browser):
 
    url_list = ["https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced",
    "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced",
    "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced",
    "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"]
    
    main_list = []
    
    for url in url_list:
      new_list = []
      
      elems = url.split('/')
      word_arr = elems[-1].split('_')
      final_name=""
      for val in word_arr:
        if(val == "enhanced"):
          val = "Hemisphere"
        final_name += val + " "
        
      new_list.append(final_name)
      
      browser.visit(url)
      browser.is_element_present_by_text('Original', wait_time=1)
      more_info_elem = browser.find_link_by_partial_text('Original')
      more_info_elem.click()

      # Parse the resulting html with soup
      html = browser.html
      img_soup = BeautifulSoup(html, 'html.parser')

      #Error Handling for Attribute Error
      try:
         # Find the relative image url
         new_list.append(img_soup.select_one('a').get("href"))
         new_list.append(url)
         main_list.append(new_list)
      except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    #img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    
    return main_list

# ### Featured Images

# Featured Image Function
def featured_image(browser):

    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

#Error Handling for Attribute Error
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
        img_url_rel
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    
    return img_url

# Scrape Mars Facts 
def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)
    
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

# End Automated Browser Session ***NOT SURE I NEED THE FOLLOWING BROWSER QUIT HERE
browser.quit()

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())


