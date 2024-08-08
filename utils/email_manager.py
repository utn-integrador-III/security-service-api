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
    message = ' Hi ' + recipient_email + ' Your verification Code to activate your account is: ' + str(code) + ' Follow this link http//:localhost:4200/activateAcc to proceed on activating your account' 
    # record the MIME type of both parts to be included in message
    part1 = MIMEText(message, 'plain')
    msg.attach(part1)


    try:
        # create a secure SSL connection with server
        server = smtplib.SMTP(config('SMTP_SERVER'),config('SMTP_PORT'))
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

def send_email_new_password(recipient_email, new_password):
    # Crea un mensaje multipart
    msg = MIMEMultipart('alternative')
    msg['From'] = config('SENDER_EMAIL')
    msg['To'] = recipient_email
    msg['Subject'] = 'Your New Password'
    
    # Define el cuerpo del mensaje con la nueva contraseña
    message = f"Hi,\n\nYour password has been successfully reset. Your new password is: {new_password}\n\nPlease use this password to log in and change your password immediately.\n\nBest regards,\nYour Support Team"
    part1 = MIMEText(message, 'plain')
    msg.attach(part1)

    try:
        # Conéctate al servidor SMTP
        server = smtplib.SMTP(config('SMTP_SERVER'), config('SMTP_PORT'))
        server.starttls()
        # Inicia sesión en tu correo electrónico
        server.login(config('SENDER_EMAIL'), config('SENDER_EMAIL_PASSWORD'))
        # Envía el correo electrónico
        server.sendmail(config('SENDER_EMAIL'), recipient_email, msg.as_string())
        print('Email has been sent!')
    except smtplib.SMTPException as e:
        print('Error: unable to send email', str(e))
    finally:
        # Cierra la conexión
        server.quit()