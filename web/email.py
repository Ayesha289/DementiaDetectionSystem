from flask import render_template
from flask_mail import Message
from . import mail


def forget_pass_email(user):

    token = user.get_reset_token()

    msg = Message()
    msg.subject = "Early Dementia Detection System Password Reset"
    msg.sender = 'dementiadetectionsystem@gmail.com'
    msg.recipients = [user.email]
    msg.html = render_template('email.html', user=user, token=token)

    mail.send(msg)