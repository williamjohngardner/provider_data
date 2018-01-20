import requests
import facebook
import twitter
import os
import config
import datetime
import json
import pprint

from InstagramAPI import InstagramAPI
from transfer import Transfer


class SocialMediaPerformance:

    def __init__(self):
        self.dealer_code = config.dealer_code
        self.fb_user_access_token = config.fb_user_access_token
        self.fb_page_access_token = config.fb_page_access_token
        self.fb_dealer_id = config.fb_dealer_id
        self.twitter_consumer_key = config.twitter_consumer_key
        self.twitter_consumer_secret = config.twitter_consumer_secret
        self.twitter_access_token = config.twitter_access_token
        self.twitter_access_token_secret = config.twitter_access_token_secret
        self.twitter_user_id = config.twitter_user_id
        self.instagram_username= config.instagram_username
        self.instagram_password = config.instagram_password
        self.yelp_client_id = config.yelp_client_id
        self.yelp_client_secret = config.yelp_client_secret
        self.yelp_username = config.yelp_username
        self.yelp_password = config.yelp_password

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

        page = graph.request('140202782671268/posts')
        page_fans = graph.request('140202782671268/insights/page_fans')
        follower_count = page_fans['data'][0]['values'][1]['value']
        posts = graph.request('140202782671268/posts?date_preset=yesterday') #pulls 25 most recent posts and is not filtering by date
        total_posts = len(posts['data'])
        page_impressions_organic = graph.request('140202782671268/insights/page_impressions_organic')
        total_reach = page_impressions_organic['data'][0]['values'][1]['value']
        page_consumptions = graph.request('140202782671268/insights/page_consumptions?date_preset=yesterday') #This is pulling in yesterday's data.
        total_engagement = page_consumptions['data'][0]['values'][0]['value']

        total_shares = []
        post_ids = posts['data']
        for i in post_ids:
            post_id = i['id']
            shares = graph.request(str(post_id) + '?fields=shares.summary(true)')
            count = shares.get('shares',{}).get('count',0)
            total_shares.append(count)
        total_advocacy = sum(total_shares)

        self.facebook_social_output = 'Dealer Code: \t' + str(self.dealer_code) + '\nChannel: \tFacebook\nTotal Follower Count: \t' + str(follower_count) + '\nTotal Posts: \t' + str(total_posts) + '\nTotal Reach: \t' + str(total_reach) + '\nTotal Engagement: \t' + str(total_engagement) + '\nTotal Advocacy: \t' + str(total_advocacy)
        return self.facebook_social_output

    def facebook_reputation(self):

        graph = facebook.GraphAPI(access_token= self.fb_page_access_token, version="2.7")

        average_rating = graph.request('140202782671268/ratings')
        pprint.pprint(average_rating)
        # total_positive = graph.request('140202782671268/insights/page_positive_feedback')
        # pprint.pprint(total_positive)
        page_negative_feedback = graph.request('140202782671268/insights/page_negative_feedback')
        total_negative = page_negative_feedback['data'][0]['values'][1]['value']
        pprint.pprint(total_negative)


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


    def yelp_api(self):

        data = {'grant_type': 'client_credentials',
                'client_id': self.yelp_client_id,
                'client_secret': self.yelp_client_secret}
        token = requests.post('https://api.yelp.com/oauth2/token', data=data)
        access_token = token.json()['access_token']
        url = 'https://api.yelp.com/v3/businesses/search'
        url_reviews = 'https://api.yelp.com/v3/businesses/tustin-toyota-tustin/reviews'
        url_business = 'https://api.yelp.com/v3/businesses/tustin-toyota-tustin-2'
        headers = {'Authorization': 'bearer %s' % access_token}
        params = {'location': 'Tustin',
                  'term': 'Toyota',
                  'sort_by': 'rating'
                 }

        resp = requests.get(url=url, params=params, headers=headers)
        review_resp = requests.get(url=url_reviews, headers=headers)
        business_resp = requests.get(url=url_business, headers=headers)

        average_rating = resp.json()['businesses'][2]['rating']
        review_times = review_resp.json()['reviews'][0]['time_created']
        total_reviews = review_resp.json()['reviews'][0]
        total_positive = None
        total_negative = None
        total_reviews = resp.json()['businesses'][2]['review_count']
        total_dealer_responses = None


        self.yelp_reputation_output = 'Dealer Code: \t' + str(self.dealer_code) + '\nChannel: \tYelp\nTotal Average Rating: \t' + str(average_rating) + '\nTotal Positive: \t' + str(total_positive) + '\nTotal Negative: \t' + str(total_negative) + '\nTotal Reviews: \t' + str(total_reviews) + '\nTotal Dealer Responses: \t' + str(total_dealer_responses)
        return self.yelp_reputation_output


    def social_activity_report(self):

        self.social_activity = str(self.facebook_api()) + '\n' + str(self.twitter_api()) + '\n' + str(self.instagram_api())
        return self.social_activity


    def social_activity_report_output(self):

        self.file_name = 'TDDSSocialActivityReport_' + self.date_strftime() + '.txt'
        output = open(self.file_name, 'w')
        output.write('Date: ' + str(self.todays_date()) + '\n' + str(self.social_activity_report()))
        output.close()
        # return self.file_name


    def reputation_management_report(self):

        self.reputation_management = str(self.yelp_api())
        return self.reputation_management


    def reputation_management_report_output(self):

        self.file_name = 'TDDSRepManagementReport_' + self.date_strftime() + '.txt'
        output = open(self.file_name, 'w')
        output.write('Date: ' + str(self.todays_date()) + '\n' + str(self.reputation_management_report()))
        output.close()


if __name__ == "__main__":
    social = SocialMediaPerformance()
    print(social.todays_date())
    # social.twitter_api()
    # social.facebook_api()
    # print(social.facebook_reputation())
    # social.instagram_api()
    # social.yelp_api()

    social.social_activity_report_output()
    # social.reputation_management_report_output()
    # send = Transfer()
    # send.ftp_social_report()
    # send.ftp_reputation_report()
