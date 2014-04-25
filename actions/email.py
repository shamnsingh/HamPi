import smtplib


def send_gmail(toaddrs, msg, username, password):
#     fromaddr = 'chessarnab@gmail.com'
#     toaddrs  = 'chessarnab@berkeley.edu'
#     #msg = 'Why,Oh why!'
#     username = 'chessarnab@gmail.com'
#     password = pwd
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()
