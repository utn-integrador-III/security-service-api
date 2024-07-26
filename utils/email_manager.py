import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from decouple import config


def send_email(recipient_email, code):
    # create a multipart message object
    msg = MIMEMultipart('alternative')
    msg['FROM'] = config('SENDER_EMAIL')
    msg['TO'] = recipient_email
    msg['Subject'] = 'Verification Code'
    message = ' Hi ' + recipient_email + 'Your verification Code to activate your account is: ' + str(code) + 'Follow this link http//:localhost:4200/activateAcc to proceed on activating your account' 
    # record the MIME type of both parts to be included in message
    part1 = MIMEText(message, 'plain')
    msg.attach(part1)

    #SMTP server configs
    smtp_server = 'smtp.office365.com'
    smtp_port = 587

    try:
        # create a secure SSL connection with server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        # Login to your outlook email
        server.login(config('SENDER_EMAIL'), config('SENDER_EMAIL_PASSWORD'))
        # send email
        server.sendmail(config('SENDER_EMAIL'), recipient_email, msg.as_string())
        print('Email Have been sent!')
    except smtplib.SMTPException as e:
        print('Error: unable to send email', str(e))
    finally:
        #close connection
        server.quit()