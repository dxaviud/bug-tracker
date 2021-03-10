import smtplib
from email.mime.text import MIMEText

def send_mail(developername, bugtype, bugpriority, bugsummary):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '515083267baa55'
    password = '7e8684fecd8425'
    message = f"<h3>New Bug Submission</h3><ul><li>developer: {developername}</li><li>Bug type: {bugtype}</li><li>Bug priority: {bugpriority}</li><li>Bug summary: {bugsummary}</li></ul>"

    sender_email = 'email1@example.com'
    receiver_email = 'email2@example.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Bug Submission'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())