import config
import json

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

class Analytics:

    def __init__(self):
        '''  The __init__ access tokens and credentials are being imported from the config.py module.
        This file must be included in the root for the script to function'''
        self.SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
        self.KEY_FILE_LOCATION = './auth.json'
        self.VIEW_ID = config.view_id

        self.DEALER_CODE = 'TEST DEALER CODE'
        self.PROFIT_CENTER = 'TEST PROFIT CENTER'
        self.ACCOUNT_NAME = 'TEST ACCOUNT NAME'
        self.PROVIDER = 'TURNKEY MARKETING'
        self.BUSINESS_CENTER = 'TEST BUSINESS CENTER'

        # self.DAILY_BUDGET # ga:adCost
        # self.MONTH_BUDGET # ga:adCost
        # self.SOURCE_MEDIUM # ga:sourceMedium
        # self.SEM_IMPRESSIONS #ga:impressions
        # self.SEM_CLICKS # ga:adClicks
        # self.SEM_CTR # ga:CTR
        # self.SEM_CPC # ga:CPC
        # self.DISPLAY_IMPRESSIONS # ga:impressions
        # self.DISPLAY_CLICKS # ga:adClicks
        # self.DISPLAY_CTR # ga:CTR
        # self.DISPLAY_CPM #ga:CPC
        # self.SEARCH_DISPLAY_IMPRESSIONS
        # self.TOTAL_CLICKS
        # self.TOTAL_CTR
        # self.PAID_SEARCH_VISITS
        # self.DISPLAY_VISITS
        # self.MOBILE_VISITS
        # self.OTHER_VISITS
        # self.ORGANIC_SEARCH_VISITS
    
    def parseResponse(self, response):
        return response['reports'][0]['data']['totals'][0]['values'][0]

    def initialize_analyticsreporting(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self.KEY_FILE_LOCATION, self.SCOPES)
        # Build the service object.
        analytics = build('analyticsreporting', 'v4', credentials=credentials)
        return analytics

    def getDailyBudget(self, analytics):
        response = analytics.reports().batchGet(
            body={
                'reportRequests': [
                {
                'viewId': self.VIEW_ID,
                'dateRanges': [{'startDate': 'yesterday', 'endDate': 'today'}],
                'metrics': [{'expression': 'ga:adCost'}]
                # 'dimensions': [{'name': 'ga:country'}]
                }]
            }
        ).execute()
        # print('RESPONSE DAILY BUDGET: ', response)
        return self.parseResponse(response)
    
    def getMonthlyBudget(self, analytics):
        response = analytics.reports().batchGet(
            body={
                'reportRequests': [
                {
                'viewId': self.VIEW_ID,
                'dateRanges': [{'startDate': '30daysAgo', 'endDate': 'today'}],
                'metrics': [{'expression': 'ga:adCost'}]
                # 'dimensions': [{'name': 'ga:country'}]
                }]
            }
        ).execute()
        # print('RESPONSE MONTHLY BUDGET: ', response)
        return self.parseResponse(response)

    def getDailyReport(self):
        self.DAILY_REPORT = self.DEALER_CODE + '\t' + self.ACCOUNT_NAME + '\t' + self.PROFIT_CENTER + '\t' + str(self.getDailyBudget(init))
        print('DAILY REPORT: ', str(self.getDailyBudget(init)))
        return self.DAILY_REPORT

    def getMonthlyReport(self):
        self.MONTHLY_REPORT = self.DEALER_CODE + '\t' + self.PROVIDER + '\t' + self.BUSINESS_CENTER + '\t' + self.ACCOUNT_NAME + '\t' + str(self.getMonthlyBudget(init))
        print('MONTHLY REPORT: ', str(self.getDailyBudget(init)))
        return self.MONTHLY_REPORT

# if __name__ == "__main__":
analytics = Analytics()
# ---------  The following call is for testing purposes.  The script runs with it commented out. -------------
init = analytics.initialize_analyticsreporting()
# response = analytics.getDailyBudget(init)
# response = analytics.getMonthlyBudget(init)
# analytics.parseResponse(response)