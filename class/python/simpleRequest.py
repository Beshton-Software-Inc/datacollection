import requests
import os     


def request(url):   
    response = requests.get(url)
    print(response.content)

def main():
   request("https://www.yahoo.com") 
 
 
if __name__=='__main__':
	main()