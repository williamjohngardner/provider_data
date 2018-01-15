import ftplib
import config


class Transfer:

    def __init__(self):
        self.USERNAME = config.ftp_username
        self.PASSWORD = config.ftp_password
        self.SERVER = config.ftp_url

    def ftp(self):
        session = ftplib.FTP(self.SERVER, self.USERNAME, self.PASSWORD)
        file = open('requirements.txt','rb')                  # file to send
        session.storbinary('STOR requirements.txt', file)     # send the file
        file.close()                                    # close file and FTP
        session.quit()

# send = Transfer()
# send.ftp()
