#!/usr/bin/env python
# coding: utf-8
# Python script to scrape an article given the url of the article and store the extracted text in a file
# Url: https://medium.com/@nick-tan/3-must-have-data-science-books-e357cdda07ea

import os
import requests
import re
import sys
#Import BeautifulSoup library
from bs4 import BeautifulSoup 
# Code ends here
rul = None          # Define the'url' as global variable
# function to get the html source text of the medium article
def get_page():
    global url
    # Code here - Ask the user to input "Enter url of a medium article: " and collect it in url
    url = input("Enter the URL of a medium article: ")  # Ask the user to input the URL
    # Code ends here
    if not re.match(r'https?://medium.com/', url):      # handling possible error
        print('Please enter a valid website, or make sure it is a medium article')
        sys.exit(1)
    # Code here - Call get method in requests object, pass url and collect it in res
    if url:
        res = requests.get(url)
        # Code ends here
        res.raise_for_status()         # Check for any HTTP request errors
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup
    else:
        print("URL is empty. Please provide a valid URL.")
        sys.exit(1)
# function to remove all the html tags and replace some with specific strings
def clean(text):
    rep = {"<br>": "\n", "<br/>": "\n", "<li>":  "\n"}
    rep = dict((re.escape(k), v) for k, v in rep.items()) 
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
    text = re.sub('\<(.*?)\>', '', text)
    return text

def collect_text(soup):
    text = f'url: {url}\n\n'
    para_text = soup.find_all('p')
    for para in para_text:
        text += f"{para.text}\n\n"
    return text

# function to save file in the current directory
def save_file(text):
    if not os.path.exists('./scraped_articles'):
        os.mkdir('./scraped_articles')
    name = url.split("/")[-1]
    fname = f'scraped_articles/{name}.txt'

    # Code here - write a file using with (2 lines)
    with open(fname, 'w', encoding='utf-8') as file:    # Write the file using with statement
        file.write(text)
    # Code ends here
    print(f'File saved in directory {fname}')

if __name__ == '__main__':
    text = collect_text(get_page())
    save_file(text)
