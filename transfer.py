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
        self.file = 'TDDSSocialActivityReport_' + now + '.txt'
        return self.file

    def ftp(self):
        session = ftplib.FTP(self.SERVER, self.USERNAME, self.PASSWORD)
        file = open(self.file,'rb')                  # file to send
        session.storbinary('STOR self.file', file)     # send the file
        file.close()                                    # close file and FTP
        session.quit()



send = Transfer()
# send.ftp()
# print(send.date_strftime())
