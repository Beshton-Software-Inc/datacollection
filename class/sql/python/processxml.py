import pandas as pd
import numpy as np
from lxml.html import parse
from urllib.request import urlopen
from pandas.io.parsers import TextParser
from lxml import objectify
import requests 
import xml.etree.ElementTree as ET
import traceback

class xmldemo:
    def __init__(self, url):
        self.__url__ = url
    
    def get_links(self):
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

        resp = requests.get('https://finance.yahoo.com/quote/AAPL/options?p=AAPL', headers=headers)
        content = resp.text
        # tree = ET.fromstring(content)
        file = open ("/tmp/my.xml", "w")
        file.write(content)
        
        # parsed = objectify.parse(file)
        # parsed = parse(content)
        # parsed = parse(urlopen('https://finance.yahoo.com/quote/AAPL/options?ltr=1', headers=headers))
        parsed = parse(file)
        doc = parsed.getroot()
        links = doc.findall('.//a')
        print(links)
        file.close()
        return tree
        
    def get_table_content(self, lnk, doc):
        # lnk = links[28]
        urls = [lnk.get('href') for lnk in doc.findall('.//a')]
        tables = doc.findall('.//table')
        calls = tables[9]
        puts = tables[13]
        call_data = self.parse_options_data(calls)
        put_data = self.parse_options_data(puts)
         
        print("total rows: {}".format(len(call_data)))
        return call_data, put_data

    def parse_options_data(table):
        rows = table.findall('.//tr')
        header = _unpack(rows[0], kind='th')
        data = [_unpack(r) for r in rows[1:]]
        return TextParser(data, names=header).get_chunk()
    
    def _unpack(row, kind='td'):
        elts = row.findall('.//%s' % kind)
        return [val.text_content() for val in elts]
    
def main():
    try:
        url = 'http://finance.yahoo.com/q/op?s=AAPL+Options'
        demo = xmldemo(url) 
        tree = demo.get_links()
        call_data, put_data = demo.get_table_content(link[28], tree)
        print("data:", call_data, put_data)
    except Exception as ex:
        print ("failed to run {}".format(ex))
        print(traceback.format_exc())
 
 
if __name__=='__main__':
	main()  