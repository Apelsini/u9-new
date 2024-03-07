import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "urls.settings")

import django
django.setup()

#from django.core.management import call_command

import json
from django.core.mail import send_mail
from authentication.models import Profile
import requests
import re


codedict = {
"100": "Continue",
"101": "Switching protocols",
"102": "Processing (WebDAV)",
"103": "Early Hints",
"200": "OK",
"201":"Created",
"202":"Accepted",
"203":"Non-Authoritative Information",
"204":"No Content",
"205":"Reset Content",
"206":"Partial Content",
"207":"Multi-Status (WebDAV)",
"208":"Already Reported (WebDAV)",
"226":"IM Used (HTTP Delta encoding)",
"300":"Multiple Choices",
"301":"Moved Permanently",
"302":"Found",
"303":"See Other",
"304":"Not Modified",
"305":"Use Proxy (Deprecated)",
"306":"unused HTTP/1.1 specification",
"307":"Temporary Redirect",
"308":"Permanent Redirect",
"400":"Bad Request",
"401":"Unauthorized",
"402":"Payment Required Experimental",
"403":"Forbidden",
"404":"Not Found",
"405":"Method Not Allowed",
"406":"Not Acceptable",
"407":"Proxy Authentication Required",
"408":"Request Timeout",
"409":"Conflict",
"410":"Gone",
"411":"Length Required",
"412":"Precondition Failed",
"413":"Payload Too Large",
"414":"URI Too Long",
"415":"Unsupported Media Type",
"416":"Range Not Satisfiable",
"417":"Expectation Failed",
"418":"I'm a teapot Some websites use this response for requests they do not wish to handle",
"421":"Misdirected Request",
"422":"Unprocessable Content (WebDAV)",
"423":"Locked (WebDAV)",
"424":"Failed Dependency (WebDAV)",
"425":"Too Early (Experimental)",
"426":"Upgrade Required",
"428":"Precondition Required",
"429":"Too Many Requests",
"431":"Request Header Fields Too Large",
"451":"Unavailable For Legal Reasons",
"500":"Internal Server Error",
"501":"Not Implemented",
"502":"Bad Gateway",
"503":"Service Unavailable",
"504":"Gateway Timeout",
"505":"HTTP Version Not Supported",
"506":"Variant Also Negotiates",
"507":"Insufficient Storage (WebDAV)",
"508":"Loop Detected (WebDAV)",
"510":"Not Extended",
"511":"Network Authentication Required"
}

#every minute notification robot, messages are taken from the notify.txt file

regex = "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
# email check https://stackabuse.com/python-validate-email-address-with-regular-expressions-regex/

def isValid(email):
    if re.fullmatch(regex, email):
      return True
    else:
      return False

def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        response = requests.post(url, json={'chat_id': chat_id, 'text': message, 'parse_mode': 'HTML'})
        print(response.text)
    except Exception as e:
        print(e)

def send_email_notification(email, message, subject):
    subject = subject
    email_from = 'support@u9.by'
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
            subject = notification['subject']

            user = Profile.objects.get(pk=user_id)
            if (user.email1cb) and (user.email1 != '-') and (isValid(user.email1)):
                send_email_notification(user.email1, message, subject)
                print('email sent to email1 of the user with id=',str(user_id),' ',str(user))
            else:
                print('wrong email1 format of the user with id=', str(user_id), ' ', str(user))
            if (user.email2cb) and (user.email2 != '-') and (isValid(user.email2)):
                send_email_notification(user.email2, message, subject)
                print('email sent to email2 of the user with id=', str(user_id), ' ', str(user))
            else:
                print('wrong email1 format of the user with id=', str(user_id), ' ', str(user))
            if user.telegram1cb:
                send_telegram_message(user.telegram1, user.telegram1chat_id, '<b>'+subject+'</b>: '+message)
                print('telegram message sent to telegram1 of the user with id=', str(user_id), ' ', str(user))
            if user.telegram2cb:
                send_telegram_message(user.telegram2, user.telegram2chat_id, '<b>'+subject+'</b>: '+message)
                print('telegram message sent to telegram2 of the user with id=', str(user_id), ' ', str(user))

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
# {"user_id": 1, "message": "Cron job is working every minute. This is a notification for uby with id=1",  "subject": "Test of cron job"}
# crontab command
# source /home/uby/virtualenv/website4/3.7/bin/activate && cd /home/uby/website4 && python notify.py > /tmp/notify.log 2>&1

def run():
    print('every 15 minute website checking robot, messages are put into the notify.txt file to form a queue for sending every minute')
    process_notifications()

if __name__ == '__main__':
    run()


