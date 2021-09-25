import pymongo
import requests, json
import pandas as pd
import numpy as np 

class mongodbDemo:
    def __init__(self):
        self.api_bearer_token = "AAAAAAAAAAAAAAAAAAAAAOYvUAEAAAAA%2BnAejXqIiEyV%2Fyuz4kR19LZenxk%3DDQF5Ogqh7dPsWX42tVzOldscP3jwlryRT1IcJqMDlf8Wy6bvuz"
        self.api_key = "SNk8QEVd2uQSmOzV7hCL4U1eO"
        self.api_secret = "1QRMJtF2TFzwKseN9sojhQPb2ibuD9NlooXTpHmEiQ6G5OfPkx"
        
    def search_tweets(self, criteria):
        def bearer_oauth(r): 
            r.headers["Authorization"] = f"Bearer {self.api_bearer_token}"
            r.headers["User-Agent"] = "v2TweetLookupPython"
            return r

        tweet_fields = "tweet.fields=lang,author_id"
        ids = "ids=1278747501642657792,1255542774432063488"
        # You can adjust ids to include a single Tweets.
        # Or you can add to up to 100 comma-separated IDs
        url = "https://api.twitter.com/2/tweets?{}&{}".format(ids, tweet_fields)
        response = requests.request("GET", url, auth=bearer_oauth)
        print(response.status_code)
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        return response.json()
    
    def insert_to_mongo(self, tweetsjson):
        con = pymongo.MongoClient('localhost', port=27017)
        tweets = con.db.tweets
        data = tweetsjson["data"]
        for tweet in data:
            tweets.insert_one(tweet)

    def query_mongo(self, s):
        con = pymongo.MongoClient('localhost', port=27017)
        tweets = con.db.tweets

        cursor = tweets.find(s)
        tweet_fields = ['created_at', 'from_user', 'id', 'text']
        result = pd.DataFrame(list(cursor), columns=tweet_fields)
        print ("results=", result)
        
def main():
    demo = mongodbDemo() 
    tweetsjson = demo.search_tweets("python")
    demo.insert_to_mongo(tweetsjson)
    demo.query_mongo({'author_id':'2244994945'}) 
  
 
if __name__=='__main__':
	main()