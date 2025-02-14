import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from celery import shared_task

from root import settings


@shared_task()
def send_email(to_send, code):
    email = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD
    # try:
    message = MIMEMultipart('alternative')
    message['Subject'] = "Verify code"
    message['From'] = email
    message['To'] = to_send


    part2 = MIMEText(f"Verify code: {code}")
    message.attach(part2)



    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(email, password)
        server.sendmail(email, [to_send], message.as_string())
        print('Success')
    return f"Success to email {to_send}!"
    # except Exception as e:
    #     print(f'Hatolik: {e}')


