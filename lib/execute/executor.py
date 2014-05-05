import smtplib, serial
from email.mime.text import MIMEText
from ..utils.parser import *

path = 'personal_data/data.dat'

class executor:
    def __init__(self):
        self.info = parseString(path)
        self.possible_commands = {'email': emailer(self.info), 'text' : texter(self.info), 'one': lighter(self.info)}
    
    def action(self, argument):
        try:
            obj = self.possible_commands[argument]
        except:
            print argument, ': command not implemented.'
            return
       
        print 'Running command...'
        obj.run()

class emailer:
    def __init__(self, info):

        self.username = info['username']
        self.password = info['password']
        self.fromaddr = info['fromaddr']
        self.toaddrs = info['toaddrs']
        self.msg = info['message']

    def run(self):
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(self.username,self.password)
        server.sendmail(self.fromaddr, self.toaddrs, self.msg)
        server.quit()
        print 'Email sent!'

class texter:

    def __init__(self, info):
        self.username = info['username']
        self.password = info['password']
        self.fromaddr = info['fromaddr']
        self.toaddrsphone = info['toaddrsphone']
        self.msg = MIMEText(info['message'])

    def run(self):
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(self.username,self.password)
        server.sendmail(self.fromaddr, self.toaddrsphone, self.msg.as_string())
        server.quit()
        print 'Text sent!'

class lighter:
    def __init__(self, info):
        self.arduino = serial.Serial(info['usb_port'], int(info['baud']))
        self.state = {True: 'H', False: 'L'}
        self.flag = True

    def run(self):
        self.arduino.write(self.state[self.flag])
        self.flag = not self.flag
        print 'Light switched.'

