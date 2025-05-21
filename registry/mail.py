import smtplib

from registry.config import email_smtp_host, email_smtp_port, email_sender, email_recipient


def send_email(recipient_email, subject, body):
    try:
        server = smtplib.SMTP(email_smtp_host, port=int(email_smtp_port))
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(email_sender, recipient_email, message)
        return True
    except smtplib.SMTPException:
        server.quit()
        return False


def send_new_vocab_email(user_id, title, homepage, description):
    subject = f"New vocabulary {title} proposed"
    body = f"A new vocabulary has been created:\n\nUser id: {user_id}\nTitle: {title}\nHomepage: {homepage}\nDescription: \n{description}"
    return send_email(email_recipient, subject, body)


def send_report_abuse_email(vocab_id, name, email, description):
    subject = "Report abuse"
    body = f"Report abuse:\n\nVocab id: {vocab_id}\nName: {name}\nEmail: {email}\nDescription: \n{description}"
    return send_email(email_recipient, subject, body)
