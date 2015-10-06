import tweepy
from pprint import pprint as pp
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter


def get_keys():
    return  {
            "consumer_key": "",
            "consumer_secret": "",
            "access_token": "",
            "access_token_secret": ""
            }

def main(handle = 'nicoteiz'):
    api = load()
    user = get_from_handle(handle, api)
    #get some user data
    stats = get_user_stats(user)
    stats['pic'] = fix_prof_img(stats['profile_image_url_https'])
    #get hashtags
    hashtags = process_hashtags(get_tweets(handle, api))
    return stats, hashtags

def get_user_stats(user=None):
    res = {}
    fields = ['profile_image_url_https', 'id_str', 'screen_name', 'followers_count', 'description', 'friends_count', 'name', 'lang', 'favourites_count']
    for field in fields:
        res[field] = user[field]
    return res
    
    
def fix_prof_img(img_url):
    if img_url[-15:-1].find('_normal.'):
        new_url = img_url[0:-15] + img_url[-15:].replace('_normal.', '.')
        return new_url

def get_from_handle(handle, api):
    if len(handle) > 0:
        try:
          user = api.get_user(handle, include_entities = 1)
          return user
        except Exception as e:
          print handle
          print e

def get_tweets(handle, api):      
    #initialize a list to hold all the tweepy Tweets
    alltweets = []    
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = handle,count=200)
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].get('id') - 1
    
    #flag to get at most 600 tweets
    loops = 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0 and loops < 3:
        print "getting tweets before %s" % (oldest)
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = handle,count=200,max_id=oldest)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].get('id') - 1
        
        #update loops
        loops += 1
        
        print "...%s tweets downloaded so far" % (len(alltweets))
        
    return alltweets
        
    
def process_hashtags(alltweets, n = 5):
    #Returns a tuple with the n most commmon hashtags
    #(and their counts) found in User tweets
    hashs = Counter()
    for tweet in alltweets:
        tags = tweet.get('entities').get('hashtags')
        for tag in tags:
            hashtag = tag['text'].lower()
            hashs[hashtag] += 1
    return hashs.most_common(n)

    
  
def load():
    tw_acc =  get_keys()
    tw_auth = tweepy.OAuthHandler(tw_acc['consumer_key'], tw_acc['consumer_secret'])
    tw_auth.set_access_token(tw_acc['access_token'], tw_acc['access_token_secret'])

    return tweepy.API(tw_auth, wait_on_rate_limit=True, parser=tweepy.parsers.JSONParser())

    
if __name__ == '__main__':
    print 'Working..'
    stats, hashtags = main()
    print stats
    print '*'*20
    print hashtags

