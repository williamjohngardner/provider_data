import requests
import facebook
import tweepy
import os
import config
import datetime

from InstagramAPI import InstagramAPI
from transfer import Transfer



class SocialMediaPerformance:

    def __init__(self):
        self.dealer_code = config.dealer_code
        self.fb_user_access_token = config.fb_user_access_token
        self.twitter_consumer_key = config.twitter_consumer_key
        self.twitter_consumer_secret = config.twitter_consumer_secret
        self.twitter_access_token = config.twitter_access_token
        self.twitter_access_token_secret = config.twitter_access_token_secret
        self.instagram_username= config.instagram_username
        self.instagram_password = config.instagram_password

    def date_strftime(self):

        now = datetime.datetime.now()
        now = now.strftime("%m-%d-%y")
        return now

    def todays_date(self):

        now = datetime.datetime.now()
        now = now.strftime("%m/%d/%Y")
        return now


    def facebook_api(self):

        graph = facebook.GraphAPI(access_token= self.fb_user_access_token)

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

        attenders = requests.get("https://graph.facebook.com/v2.7/"+eventid+"/attending?access_token="+self.fb_user_access_token+"&limit="+str(attenderscount))
        attenders_json = attenders.json()

        print(attenders_json)


    def twitter_api(self):

        auth = tweepy.OAuthHandler(self.twitter_consumer_key, self.twitter_consumer_secret)
        auth.set_access_token(self.twitter_access_token, self.twitter_access_token_secret)

        api = tweepy.API(auth)

        user = api.get_user('williamjgardner')
        status = api.get_status('888376794780401664')
        dealer_code = user.screen_name
        follower_count = str(user.followers_count)
        total_posts = str(user.statuses_count) #need to figure out how to filter status count by specific day
        total_reach = str(user.followers_count)
        total_engagement = None
        retweets = api.retweets_of_me()
        total_advocacy = retweets.count
        # a = 0
        # for i in total_advocacy:
        #     a += 1
        #     print(i.index)
        # print(str(a))

        # print('Dealer Code: ' + dealer_code)
        # print('Channel: Twitter')
        # print('Total Follower Count: ' + follower_count)
        # print('Total Posts: ' + total_posts)
        # print('Total Reach: ' + total_reach)
        # print('Total Engagement: TBD')
        # print('Total Advocacy: ' + str(total_advocacy))
        # print(dir(retweets))

        print('Dealer Code: ' + dealer_code + '\nChannel: Twitter\nTotal Follower Count: ' + follower_count + '\nTotal Posts: ' + total_posts + '\nTotal Reach: ' + total_reach + '\nTotal Engagement: TBD\nTotal Advocacy: ' + str(total_advocacy))

    def instagram_api(self):

        api = InstagramAPI(self.instagram_username, self.instagram_password)
        api.login() # login
        api.tagFeed("cat") # get media list by tag #cat
        media_id = api.LastJson # last response JSON
        api.like(media_id["ranked_items"][0]["pk"]) # like first media
        api.getUserFollowers(media_id["ranked_items"][0]["user"]["pk"]) # get first media owner followers

    def social_activity_report(self):

        self.social_activity = None

    def social_activity_report_output(self):

        self.file_name = 'TDDSSocialActivityReport_' + social.date_strftime() + '.txt'
        output = open(self.file_name, 'w')
        return self.file_name

if __name__ == "__main__":
    social = SocialMediaPerformance()
    print(social.todays_date())
    social.twitter_api()
    # social.facebook_api()
    # social.instagram_api()
    # social.document_output()
    # send = Transfer()
    # send.ftp()
    print(social.social_activity_report_output())
