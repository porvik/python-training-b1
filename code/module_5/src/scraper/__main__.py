import os
import requests
import selenium.webdriver
import selenium
import json

def main():
    url="https://python-training-b1.porvik.repl.co/files"
    # url="https://www.merriam-webster.com/dictionary/happy"

    """
    If we would be to access URL using requests library then following would be sufficient
    but we would still need to parse the whole page using some XML / XHTML parser, maybe simple XPATH
    expression would be sufficient.
    """
    # page_content = requests.get(url).text

    """
    Alternativelly you can use selenium to fetch the page "as human would do" and get you
    directly the element in question. You could also use XPATH here to achieve higher precision
    in element matching. In order to run this in you laptop you will need Firefox driver
    (see https://www.selenium.dev/selenium/docs/api/javascript/module/selenium-webdriver/firefox.html)
    """
    webdriver = selenium.webdriver.Firefox()
    webdriver.get(url)
    page_content = webdriver.find_element_by_tag_name('body').text

    print(page_content)


if __name__ == '__main__':
    main()
