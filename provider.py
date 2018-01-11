import requests
import facebook
import tweepy
import os
import config



def facebook_api():

    fb_user_access_token = config.fb_user_access_token

    graph = facebook.GraphAPI(access_token= fb_user_access_token)

    events = graph.request('/search?q=Poetry&type=event&limit=10000')

    eventList = events['data']

    eventid = eventList[1]['id']

    event1 = graph.get_object(id=eventid,
     fields='attending_count,can_guests_invite,category,cover,declined_count,description,end_time,guest_list_enabled,interested_count,is_canceled,is_page_owned,is_viewer_admin,maybe_count,noreply_count,owner,parent_group,place,ticket_uri,timezone,type,updated_time')
    attenderscount = event1['attending_count']
    declinerscount = event1['declined_count']
    interestedcount = event1['interested_count']
    maybecount = event1['maybe_count']
    noreplycount = event1['noreply_count']

    attenders = requests.get("https://graph.facebook.com/v2.7/"+eventid+"/attending?access_token="+fb_user_access_token+"&limit="+str(attenderscount))
    attenders_json = attenders.json()

    print(attenders_json)


def twitter_api():

    twitter_consumer_key = config.twitter_consumer_key
    twitter_consumer_secret = config.twitter_consumer_secret
    twitter_access_token = config.twitter_access_token
    twitter_access_token_secret = config.twitter_access_token_secret

    auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
    auth.set_access_token(twitter_access_token, twitter_access_token_secret)

    api = tweepy.API(auth)

    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print(tweet.text)



twit = twitter_api()
# face = facebook_api()
