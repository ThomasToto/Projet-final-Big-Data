# -*- coding: utf-8 -*-
"""
Created on Sun Dec 19 15:09:04 2021

@author: Thomas
"""

import tweepy
import json
from kafka import KafkaProducer


from keys import API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


producer = KafkaProducer(bootstrap_servers='localhost:9092')


# Création d'un StreamListener

class MyStreamListener(tweepy.StreamListener):

    def on_data(self, raw_data):
        self.process_data(raw_data)
        return True

    def process_data(self, raw_data):
        data = json.loads(raw_data)
        try:
            if 'place' in data and data['place']:
                producer.send("quickstart-events", str.encode(raw_data))
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status_code):
        print(status_code)


# Création d'un stream
class MyStream():

    def __init__(self, auth, listener):
        self.stream = tweepy.Stream(auth=auth, listener=listener)

    def start(self):
        self.stream.sample(stall_warnings=None)



if __name__ == "__main__":

    listener = MyStreamListener()

    auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    stream = MyStream(auth, listener)
    stream.start()

