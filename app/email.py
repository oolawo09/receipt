from threading import Thread
from flask import render_template
from flask_mail import Message
from app import app, mail


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    #mail.send(msg) Skipping sending out an actual email until I figure out authentication for an account


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)