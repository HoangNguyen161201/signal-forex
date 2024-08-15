import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(receiver, subject, content):
    sender_email = 'hoanghpang@gmail.com'
    password = 'nurvpaqbcgxruyqm'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver
    msg['Subject'] = subject

    # Nội dung email
    msg.attach(MIMEText(content , 'plain'))

    # Thiết lập kết nối với server Gmail
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver, text)  # Gửi email
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()

