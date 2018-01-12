import requests
import facebook
import tweepy
import os
import config

class SocialMediaPerformance:

    def __init__(self):
        self.twitter_consumer_key = config.twitter_consumer_key
        self.twitter_consumer_secret = config.twitter_consumer_secret
        self.twitter_access_token = config.twitter_access_token
        self.twitter_access_token_secret = config.twitter_access_token_secret

    def facebook_api(self):

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


    def twitter_api(self):

        auth = tweepy.OAuthHandler(self.twitter_consumer_key, self.twitter_consumer_secret)
        auth.set_access_token(self.twitter_access_token, self.twitter_access_token_secret)

        api = tweepy.API(auth)

        user = api.get_user('williamjgardner')
        retweets = api.retweets_of_me(count=1)
        status = api.get_status('888376794780401664')

        print('Data for User: ' + user.screen_name)
        print('Total Follower Count: ' + str(user.followers_count))
        print(status.text)
        # for retweet in retweets:
        #     print(retweet)


    def instagram_api(self):

        from InstagramAPI import InstagramAPI

        instagram_username= config.instagram_username
        instagram_password = config.instagram_password

        api = InstagramAPI(instagram_username, instagram_password)
        api.login() # login
        api.tagFeed("cat") # get media list by tag #cat
        media_id = api.LastJson # last response JSON
        api.like(media_id["ranked_items"][0]["pk"]) # like first media
        api.getUserFollowers(media_id["ranked_items"][0]["user"]["pk"]) # get first media owner followers

    def document_output(self):

        total_fans = twitter_api.retweets
        # tab_doc = {}'\t'{}'\t'{}'\t'{}'\n'.format()
        print('Total Fans: ' + str(total_fans))


social = SocialMediaPerformance()
social.twitter_api()
# social.facebook_api()
social.instagram_api()
# social.document_output()
