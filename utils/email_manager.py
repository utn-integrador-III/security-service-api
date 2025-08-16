# utils/email_manager.py
from decouple import config
from azure.communication.email import EmailClient

def _email_client():
    conn_str = config("ACS_CONNECTION_STRING")
    return EmailClient.from_connection_string(conn_str)

def _send_with_acs(subject: str, plain_text: str, html: str, to_address: str):
    client = _email_client()
    sender = config("ACS_SENDER_ADDRESS")
    msg = {
        "senderAddress": sender,
        "recipients": {"to": [{"address": to_address}]},
        "content": {"subject": subject, "plainText": plain_text, "html": html},
    }
    reply_to = config("REPLY_TO_EMAIL", default=None)
    if reply_to:
        msg["replyTo"] = [{"address": reply_to}]

    poller = client.begin_send(msg)
    result = poller.result()  # LRO: espera hasta que ACS acepte el envío
    # Opcional: puedes loguear result.message_id si lo necesitas
    return result

def send_email(recipient_email: str, code: str):
    """
    Envía el correo de verificación de cuenta.
    """
    # corrige el link (estaba "http//:..."): usa http://localhost:5002/activateAcc
    activate_link = f"http://localhost:5002/activateAcc?email={recipient_email}&code={code}"

    subject = "Verification Code"
    plain = (
        f"Hi {recipient_email}\n\n"
        f"Your verification code to activate your account is: {code}\n"
        f"Follow this link to continue: {activate_link}\n\n"
        "If you did not request this, you can ignore this email."
    )
    html = f"""
    <p>Hi <strong>{recipient_email}</strong>,</p>
    <p>Your verification code to activate your account is: <strong>{code}</strong></p>
    <p>
        Click here to continue: <a href="{activate_link}">{activate_link}</a>
    </p>
    <p style="color:#666;font-size:12px">If you did not request this, you can ignore this email.</p>
    """

    try:
        _send_with_acs(subject, plain, html, recipient_email)
        print("Verification email sent via ACS.")
    except Exception as e:
        # loguea bien el error en tu app
        print("Error sending verification email via ACS:", str(e))
        raise

def send_email_new_password(recipient_email: str, new_password: str):
    """
    Envía el correo con la nueva contraseña generada.
    """
    subject = "Your New Password"
    plain = (
        "Hi,\n\n"
        f"Your password has been successfully reset. Your new password is: {new_password}\n\n"
        "Please log in and change your password immediately.\n\n"
        "Best regards,\nSupport Team"
    )
    html = f"""
    <p>Hi,</p>
    <p>Your password has been successfully reset. Your new password is:
       <strong>{new_password}</strong></p>
    <p>Please log in and change your password immediately.</p>
    <p>Best regards,<br/>Support Team</p>
    """

    try:
        _send_with_acs(subject, plain, html, recipient_email)
        print("Password reset email sent via ACS.")
    except Exception as e:
        print("Error sending password reset email via ACS:", str(e))
        raise