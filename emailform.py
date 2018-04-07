def send_email(filename, email_to):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email import encoders
    from config import Email


    email_user = Email.email_from
    subject = 'Python'

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_to
    msg['Bcc'] = islempos.eshop@gmail.com
    msg['Subject'] = subject

    body = '''\
    <html>
    <head>
        <meta charset="utf-8">
    </head>
    <body>
        <p>
            Sveiki,<br><br>
            prisegtuke rasite sąskaitą apmokėjimui bei mokėjimui reikalingus rekvizitus.<br><br>
            Ačiū kad perkate.<br><br><br>
            Šviečianti „Iš lempos“ komanda
        </p>
    </body>
    </html>
    '''
    msg.attach(MIMEText(body,'html')) # Reikia sukurti laisko HTML
    text = msg.as_string()

    attachment = open(filename, 'rb')

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename= ' + filename)

    msg.attach(part)
    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_user, Email.psw)

    server.sendmail(email_user, email_to, text)
    server.quit()


