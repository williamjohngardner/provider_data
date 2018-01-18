import requests
import facebook
import twitter
import os
import config
import datetime
import json

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

        graph = facebook.GraphAPI(access_token= self.fb_user_access_token, version="2.7")

        page = graph.get_object(id='419502714752257', fields='fan_count')
        # print('Total Fan Count: ')
        follower_count = page['fan_count']

        posts = graph.request('419502714752257/posts?fields=id&limit=100')
        # print('Total Post Count: ')
        total_posts = len(posts['data'])

        page_impressions_organic = graph.request('419502714752257/insights/page_impressions_organic')
        total_reach = page_impressions_organic['data'][0]['values'][0]['value']
        # print('Total Reach: ')
        # print(total_reach)

        page_consumptions = graph.request('419502714752257/insights/page_consumptions?date_preset=yesterday')
        total_engagement = page_consumptions['data'][0]['values'][0]['value']
        # print('Total Engagement: ')
        # print(total_engagement)

        # post_ids = posts['data']
        # for i in post_ids:
        #     share_ids = i['id']
        #     for c in share_ids:
        #         shares = graph.request(str(share_ids) + '?fields=shares.summary(true)')
        #     shares_json = json.dumps(shares)
        #     print(shares_json['id'])
            # for j in shares_json:
            #     if shares_json['shares']:
            #         print(j)
                    # total_shares += j['shares']['count']
        # print('Total Shares: ')
        # print(total_shares)
            # for j in shares.keys():
            #     if j == 'shares':
            #         print(j)
        total_advocacy = None

        self.facebook_social_output = 'Dealer Code: \t' + str(self.dealer_code) + '\nChannel: \tFacebook\nTotal Follower Count: \t' + str(follower_count) + '\nTotal Posts: \t' + str(total_posts) + '\nTotal Reach: \t' + str(total_reach) + '\nTotal Engagement: \t' + str(total_engagement) + '\nTotal Advocacy: \t' + str(total_advocacy)
        return self.facebook_social_output


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
        # newest_retweet = api.GetRetweetsOfMe(count=1)
        # tweet = newest_retweet.index('ScreenName')
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

        username_id = api.username_id   #calls Instagram username ID
        follower_count = len(api.getTotalSelfFollowers())   #returns the length of the list of total followers
        total_posts = len(api.getTotalSelfUserFeed(username_id))    #returns the length of the list of total posts
        total_reach = follower_count
        total_comments = api.getTotalSelfUserFeed(username_id)
        engagement_comments = 0
        engagement_likes = 0
        for comment in total_comments:
            engagement_comments += comment['comment_count']
            engagement_likes += comment['like_count']
        total_engagement = engagement_comments + engagement_likes
        total_advocacy = total_engagement

        api.logout() #logout
        self.instagram_social_output = 'Dealer Code: \t' + str(self.dealer_code) + '\nChannel: \tInstagram\nTotal Follower Count: \t' + str(follower_count) + '\nTotal Posts: \t' + str(total_posts) + '\nTotal Reach: \t' + str(total_reach) + '\nTotal Engagement: \t' + str(total_engagement) + '\nTotal Advocacy: \t' + str(total_advocacy)
        return self.instagram_social_output


    def social_activity_report(self):

        self.social_activity = str(self.facebook_api()) + '\n' + str(self.twitter_api())
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
    # social.social_activity_report()
    social.facebook_api()
    # social.instagram_api()

    social.social_activity_report_output()
    # send = Transfer()
    # send.ftp()
