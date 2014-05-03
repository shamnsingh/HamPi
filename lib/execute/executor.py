import smtplib
from email.mime.text import MIMEText

class executor:
    def __init__(self, argument, data):
        self.command = argument
        self.data = data
        self.possible_commands = {'email': emailer(self.data), 'text' : texter(self.data) }
    def action(self):
        obj = self.possible_commands[self.command]
        obj.run()

class emailer:
    def __init__(self, data):
        self.username = 'username'
        self.password = 'password'
        self.fromaddr = 'username@gmail.com'
        self.toaddrs = 'username@domain.com'
        self.msg = data
    def run(self):
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(self.username,self.password)
        server.sendmail(self.fromaddr, self.toaddrs, self.msg.as_string())
        server.quit()
class texter:
    def __init__(self, data):
        self.username = 'username'
        self.password = 'password'
        self.fromaddr = 'username@gmail.com'
        self.toaddrs = 'phonenumber@vtext.com'
        self.msg = MIMEText(str(data))
    def run(self):
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(self.username,self.password)
        server.sendmail(self.fromaddr, self.toaddrs, self.msg.as_string())
        server.quit()
