import requests
import facebook
import twitter
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
        self.twitter_user_id = config.twitter_user_id
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

        api = twitter.Api(consumer_key=self.twitter_consumer_key,
                          consumer_secret=self.twitter_consumer_secret,
                          access_token_key=self.twitter_access_token,
                          access_token_secret=self.twitter_access_token_secret)

        user = api.GetUser(self.twitter_user_id)
        statuses = api.GetUserTimeline(self.twitter_user_id)
        follower_count = user.followers_count
        total_posts = user.statuses_count       #need to figure out how to filter status count by specific day
        total_reach = user.followers_count
        retweets = api.GetRetweetsOfMe(count=100)
        replies = api.GetReplies()
        mentions = api.GetMentions()
        favorites = api.GetFavorites()
        total_engagement = len(replies) + len(retweets) + len(mentions) + len(favorites)
        total_advocacy = len(retweets)

        self.twitter_social_output = 'Dealer Code: \t' + str(self.dealer_code) + '\nChannel: \tTwitter\nTotal Follower Count: \t' + str(follower_count) + '\nTotal Posts: \t' + str(total_posts) + '\nTotal Reach: \t' + str(total_reach) + '\nTotal Engagement: \t' + str(total_engagement) + '\nTotal Advocacy: \t' + str(total_advocacy)
        return self.twitter_social_output


    def instagram_api(self):

        api = InstagramAPI(self.instagram_username, self.instagram_password)
        api.login() # login
        api.tagFeed("cat") # get media list by tag #cat
        media_id = api.LastJson # last response JSON
        api.like(media_id["ranked_items"][0]["pk"]) # like first media
        api.getUserFollowers(media_id["ranked_items"][0]["user"]["pk"]) # get first media owner followers


    def social_activity_report(self):

        self.social_activity = self.twitter_api()
        return self.social_activity


    def social_activity_report_output(self):

        self.file_name = 'TDDSSocialActivityReport_' + self.date_strftime() + '.txt'
        output = open(self.file_name, 'w')
        output.write('Date: ' + str(self.todays_date()) + '\n' + str(self.social_activity_report()))
        output.close()
        # return self.file_name


if __name__ == "__main__":
    social = SocialMediaPerformance()
    print(social.todays_date())
    social.twitter_api()
    social.social_activity_report()
    # social.facebook_api()
    # social.instagram_api()

    social.social_activity_report_output()
    send = Transfer()
    send.ftp()
