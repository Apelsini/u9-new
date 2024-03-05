import os
import json
from django.core.mail import send_mail
from authentication.models import Profile
import requests
import re

#every minute notification robot, messages are taken from the notify.txt file

regex = "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
# email check https://stackabuse.com/python-validate-email-address-with-regular-expressions-regex/

def isValid(email):
    if re.fullmatch(regex, email):
      return True
    else:
      return False

def send_telegram_message(chat_id, token, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(url, data=data)
    return response.json()

def send_email_notification(email, message):
    subject = 'Notification'
    email_from = 'adm@u9.by'
    recipient_list = [email,]
    send_mail(subject, message, email_from, recipient_list)

def process_notifications():
    with open('notify.txt', 'r') as file:
        lines = file.readlines()

    with open('notify.txt', 'w') as file:
        for line in lines:
            notification = json.loads(line)
            user_id = notification['user_id']
            message = notification['message']

            user = Profile.objects.get(pk=user_id)
            if (user.email1cb) and (user.email1 != '-') and (user.email1):
                send_email_notification(user.email1, message)
            if user.email2cb:
                send_email_notification(user.email2, message)
            if user.telegram1cb:
                send_telegram_message(user.telegram1, message)
            if user.telegram2cb:
                send_telegram_message(user.telegram2, message)

            # Do not write this notification back to the file
            lines.remove(line)

        # Write the remaining notifications back to the file
        file.writelines(lines)

# In this script, process_notifications reads each line from notify.txt,
# parses it as a JSON object, retrieves the user associated with the user_id in the notification,
# sends the notification message to the user’s email addresses and Telegram bots, and then removes the notification from notify.txt.
#
# Please replace get_user_by_id(id) and send_telegram_message(token, message) with your actual functions
# to get a user by ID and to send a message to a Telegram bot. Also, don’t forget to configure
# your email settings in your Django settings file. For more information, you can refer to the Django documentation on sending email.
# The notify.txt file is expected to contain one JSON object per line, where each JSON object represents a notification. Each notification should have a user_id and a message. Here’s an example of how the notify.txt file might look:
#
# JSON
#
# {"user_id": 1, "message": "This is a notification for user 1"}
# {"user_id": 2, "message": "This is a notification for user 2"}
# {"user_id": 3, "message": "This is a notification for user 3"}

def run():
    print('every minute notification robot, messages are taken from the notify.txt file')
