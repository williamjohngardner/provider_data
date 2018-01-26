import ftplib
import config
import datetime


class Transfer:

    def __init__(self):
        self.USERNAME = config.ftp_username
        self.PASSWORD = config.ftp_password
        self.SERVER = config.ftp_url

    def date_strftime(self):

        now = datetime.datetime.now()
        now = now.strftime("%m-%d-%y")
        return now

    def ftp_social_report(self):
        file_name = 'TDDSSocialActivityReport_' + self.date_strftime() + '.txt'
        stor = 'STOR ' + file_name
        session = ftplib.FTP(self.SERVER, self.USERNAME, self.PASSWORD)
        file = open(str(file_name),'rb')                    # file to send
        session.storbinary(str(stor), file)                 # send the file
        file.close()                                        # close file and FTP
        session.quit()

    def ftp_reputation_report(self):
        file_name = 'TDDSRepManagementReport_' + self.date_strftime() + '.txt'
        stor = 'STOR ' + file_name
        session = ftplib.FTP(self.SERVER, self.USERNAME, self.PASSWORD)
        file = open(str(file_name),'rb')                     # file to send
        session.storbinary(str(stor), file)                  # send the file
        file.close()                                         # close file and FTP
        session.quit()
