import sys
import numpy as np
import pandas as pd
import requests 
import matplotlib.pyplot as plt 
class webscrape:
    def __init__(self):
        pass
    
    def scape_url(self, url):
        resp = requests.get(url)
        data = resp.json()
        issues = pd.DataFrame(data, columns=['number', 'title',
                                     'labels', 'state'])
        print (data)
        

def main():
    url = 'https://api.github.com/repos/pandas-dev/pandas/issues'
    scraper = webscrape()
    scraper.scape_url(url)
    
if __name__ == '__main__':
    main( )