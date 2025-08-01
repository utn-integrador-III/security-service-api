import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from decouple import config

def send_email(recipient_email, code, subject='Verification Code'):
    msg = MIMEMultipart('alternative')
    msg['From'] = config('SENDER_EMAIL')
    msg['To'] = recipient_email
    msg['Subject'] = subject
    message = (
        f"Hi {recipient_email},\n\n"
        f"Your verification code to activate your account is: {code}\n"
        f"Please enter this code in the app to activate your account."
    )
    part1 = MIMEText(message, 'plain')
    msg.attach(part1)

    try:
        server = smtplib.SMTP(config('SMTP_SERVER'), int(config('SMTP_PORT')))
        server.starttls()
        server.login(config('SENDER_EMAIL'), config('SENDER_EMAIL_PASSWORD'))
        server.sendmail(config('SENDER_EMAIL'), recipient_email, msg.as_string())
        print('Email has been sent!')
    except smtplib.SMTPException as e:
        print('Error: unable to send email', str(e))
    finally:
        server.quit()

def send_email_new_password(recipient_email, new_password):
    msg = MIMEMultipart('alternative')
    msg['From'] = config('SENDER_EMAIL')
    msg['To'] = recipient_email
    msg['Subject'] = 'Your New Password'
    message = (
        f"Hi,\n\n"
        f"Your password has been successfully reset. Your new password is: {new_password}\n\n"
        f"Please use this password to log in and change your password immediately.\n\n"
        f"Best regards,\nYour Support Team"
    )
    part1 = MIMEText(message, 'plain')
    msg.attach(part1)

    try:
        server = smtplib.SMTP(config('SMTP_SERVER'), int(config('SMTP_PORT')))
        server.starttls()
        server.login(config('SENDER_EMAIL'), config('SENDER_EMAIL_PASSWORD'))
        server.sendmail(config('SENDER_EMAIL'), recipient_email, msg.as_string())
        print('Email has been sent!')
    except smtplib.SMTPException as e:
        print('Error: unable to send email', str(e))
    finally:
        server.quit()
