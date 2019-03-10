import requests
import os
import config
import datetime
import json
import pprint

from transfer import Transfer
from analytics import Analytics
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


class SuburbanCollection:

    def __init__(self):
        '''  The __init__ access tokens and credentials are being imported from the config.py module.
        This file must be included in the root for the script to function'''
        self.SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
        self.KEY_FILE_LOCATION = './auth.json'
        self.VIEW_ID = config.view_id
        self.analytics = Analytics()

    def date_strftime(self):
        now = datetime.datetime.now()
        now = now.strftime("%m-%d-%y")
        return now

    def todays_date(self):
        now = datetime.datetime.now()
        now = now.strftime("%m/%d/%Y")
        return now

    def yesterdays_date(self):
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        yesterday.strftime('%d+%B+%Y')
        return yesterday

    def daily_activity_report(self):
        self.DAILY_REPORT = str(self.analytics.getDailyReport())
        return self.DAILY_REPORT

    def daily_activity_report_output(self):
        self.file_name = 'SuburbanDigitalAdReport_' + self.date_strftime() + '.txt'
        output = open(self.file_name, 'w')
        output.write('Date: ' + str(self.todays_date()) + '\n' + str(self.daily_activity_report()))
        output.close()


    def monthly_activity_report(self):
        self.MONTHLY_REPORT = str(self.analytics.getMonthlyReport())
        return self.MONTHLY_REPORT


    def monthly_activity_report_output(self):
        self.file_name = 'MonthlyDealerBudgetTemplate_' + self.date_strftime() + '.txt'
        output = open(self.file_name, 'w')
        output.write('Date: ' + str(self.todays_date()) + '\n' + str(self.monthly_activity_report()))
        output.close()

if __name__ == "__main__":
    suburban = SuburbanCollection()
    print(suburban.todays_date())
    suburban.daily_activity_report_output()
    suburban.monthly_activity_report_output()
    send = Transfer()
    send.ftp_daily_report()
