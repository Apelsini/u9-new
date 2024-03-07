import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "urls.settings")

import django
django.setup()

#from django.core.management import call_command

import json
from django.core.mail import send_mail
from authentication.models import Profile
from polls.models import Webrecords
import requests
import re
from datetime import datetime


codedict = {
"100": "⏳ Continue",
"101": "⏳ Switching protocols",
"102": "⏳ Processing (WebDAV)",
"103": "⏳ Early Hints",
"200": "✅ OK",
"201":"⚠ Created",
"202":"✅ Accepted",
"203":"⚠ Non-Authoritative Information",
"204":"⚠ No Content",
"205":"⚠ Reset Content",
"206":"⚠ Partial Content",
"207":"✅ Multi-Status (WebDAV)",
"208":"✅ Already Reported (WebDAV)",
"226":"✅ IM Used (HTTP Delta encoding)",
"300":"🔱 Multiple Choices",
"301":"🔱 Moved Permanently",
"302":"🔱 Found",
"303":"🔱 See Other",
"304":"🔱 Not Modified",
"305":"🔒 Use Proxy (Deprecated)",
"306":"unused HTTP/1.1 specification",
"307":"🔱 Temporary Redirect",
"308":"🔱 Permanent Redirect",
"400":"❌ Bad Request",
"401":"❌ Unauthorized",
"402":"💰 Payment Required Experimental",
"403":"❌ Forbidden",
"404":"❌ Not Found",
"405":"❌ Method Not Allowed",
"406":"❌ Not Acceptable",
"407":"❓ Proxy Authentication Required",
"408":"🕗 Request Timeout",
"409":"⚠ Conflict",
"410":"👻 Gone",
"411":"❓ Length Required",
"412":"❌ Precondition Failed",
"413":"📈 Payload Too Large",
"414":"🐍 URI Too Long",
"415":"❓ Unsupported Media Type",
"416":"🧺 Range Not Satisfiable",
"417":"🧺 Expectation Failed",
"418":"☕ I'm a teapot. Some websites use this response for requests they do not wish to handle",
"421":"🔱 Misdirected Request",
"422":"📈 Unprocessable Content (WebDAV)",
"423":"🔒 Locked (WebDAV)",
"424":"🔒 Failed Dependency (WebDAV)",
"425":"⏳ Too Early (Experimental)",
"426":"❓ Upgrade Required",
"428":"❓ Precondition Required",
"429":"🧺 Too Many Requests",
"431":"🐍 Request Header Fields Too Large",
"451":"⚠ Unavailable For Legal Reasons",
"500":"❌ Internal Server Error",
"501":"❓ Not Implemented",
"502":"❌ Bad Gateway",
"503":"❌ Service Unavailable",
"504":"🕗 Gateway Timeout",
"505":"⚠ HTTP Version Not Supported",
"506":"⚠ Variant Also Negotiates",
"507":"🧺 Insufficient Storage (WebDAV)",
"508":"🧺 Loop Detected (WebDAV)",
"510":"🧺 Not Extended",
"511":"🔒 Network Authentication Required"
}

#every 15 minutes website checking robot,
# Logging messages are sent to cronlog.txt to be displayed on the Webchecker page
# notifications message are sent to notify.txt
# {"user_id": 1, "message": "Cron job is working every minute. This is a notification for uby with id=1",  "subject": "Test of cron job"}

# iterable
# POLLING_CHOICES =(
# ("1", "Every 15 min"),
# ("2", "Every 30 min"),
# ("3", "Every 60 min"),
# ("4", "Every 2 hours"),
# ("5", "Every 4 hours"),
# ("6", "Every 8 hours"),
# ("7", "Every 24 hours"),
# ("8", "Every 2 days"),
# ("9", "Every 4 days"),
# ("10", "Every 7 days"),
# )

PF = '1' #polling frequency constant - refer to POLLING CHOICES constant to configure
PFS = 'every 15 min'

def process_notifications():
    starting_datetime = datetime.now()
    counter = 0
    lines = []
    webrecordsall = Webrecords.objects.all()
    print("<<    "+str(webrecordsall.count()) + ' records found    >>')
    profiles = Profile.objects.all()
    print("<    "+str(profiles.count()) + ' user profiles found    >')
    for profile in profiles:
        webrecords = webrecordsall.filter(author=profile.user)
        print(profile.user.username+": "+str(webrecords.count())+' records filtered')
        if webrecords:
            for webrecord in webrecords:
                if webrecord.polling_frequency == PF:   #polling frequency matches
                    if webrecord.notifycb:      #user asked to notify on response codes - then process
                        try:
                            r = requests.get(webrecord.url)
                            rcode = r.status_code
                            msg1 = "U9.by Webchecker bot pinging the" + webrecord.url + " " + PFS
                            msg2 = "The last ping at " + str(starting_datetime) + " returned response code " + str(
                                rcode) + " " + codedict[str(rcode)]
                            msg3 = "The webchecker bot was set up by user " + str(profile.user.username) + " " + str(
                                profile.user.email) + " https://u9.by/a/webchecker/editdelete/" + str(webrecord.id)
                            msg = msg1 + msg2 + msg3
                        except requests.exceptions.MissingSchema:
                            r = requests.get('https://'+webrecord.url)
                            rcode = r.status_code
                            msg1 = "U9.by Webchecker bot pinging the" + webrecord.url + " " + PFS
                            msg2 = "The last ping at " + str(starting_datetime) + " returned response code " + str(
                                rcode) + " " + codedict[str(rcode)]
                            msg3 = "The webchecker bot was set up by user " + str(profile.user.username) + " " + str(
                                profile.user.email) + " https://u9.by/a/webchecker/editdelete/" + str(webrecord.id)
                            msg = msg1 + msg2 + msg3
                        except Exception as e:
                            msg1 = "U9.by Webchecker bot pinging the"+webrecord.url+" "+PFS
                            msg2 = "The last ping at "+str(starting_datetime)+" returned EXCEPTION "+str(e)
                            msg3 = "The webchecker bot was set up by user "+str(profile.user.username)+" "+str(profile.user.email)+" https://u9.by/a/webchecker/editdelete/"+str(webrecord.id)
                            msg = msg1 + msg2 + msg3
                            dict = {"user_id": profile.user.id,
                                    "message": msg,
                                    "subject": "U9 Webchecker raised EXCEPTION for " + webrecord.url}
                            lines.append(json.dumps(dict))
                            rcode = 0
                        counter = counter+1
                        # {"user_id": 1, "message": "Cron job is working every minute. This is a notification for uby with id=1",  "subject": "Test of cron job"}
                        dict = {"user_id": profile.user.id,
                            "message" : msg,
                            "subject": "U9 Webchecker received code "+str(rcode)+" from "+webrecord.url}
                        if str(rcode)[0] =="1" and webrecord.code100cb:
                            lines.append(json.dumps(dict))
                        if str(rcode)[0] =="2" and webrecord.code200cb:
                            lines.append(json.dumps(dict))
                        if str(rcode)[0] == "3" and webrecord.code300cb:
                            lines.append(json.dumps(dict))
                        if str(rcode)[0] == "4" and webrecord.code400cb:
                            lines.append(json.dumps(dict))
                        if str(rcode)[0] == "5" and webrecord.code500cb:
                            lines.append(json.dumps(dict))
    with open('notify.txt', 'r') as file:
        existinglines = file.readlines()
        existinglines.extend(lines)
    with open('notify.txt', 'w') as file:
        file.writelines(existinglines)
        print('+++++  notify.txt file formed')
    ending_datetime = datetime.now()
    with open('cronlog.txt', 'r') as file:
        existinglines = file.readlines()
        existinglines.extend('Cron job for '+PFS+' started at: '+str(starting_datetime)+' ended at: '+str(ending_datetime)+' pinged '+str(counter)+' webrecords.')
    with open('cronlog.txt', 'w') as file:
        file.writelines(existinglines[1:])  #removing zero line
        print('+++++  cronlog.txt file appended with:'+'Cron job for '+PFS+' started at: '+str(starting_datetime)+' ended at: '+str(ending_datetime)+' pinged '+str(counter)+' webrecords.')

# The notify.txt file is expected to contain one JSON object per line, where each JSON object represents a notification. Each notification should have a user_id and a message. Here’s an example of how the notify.txt file might look:
#
# JSON
#
# {"user_id": 1, "message": "Cron job is working every minute. This is a notification for uby with id=1",  "subject": "Test of cron job"}
# crontab command
# source /home/uby/virtualenv/website4/3.7/bin/activate && cd /home/uby/website4 && python notify.py > /tmp/notify.log 2>&1

def run():
    print(PFS+' website checking robot, messages are put into the notify.txt file to form a queue for sending every minute')
    process_notifications()

if __name__ == '__main__':
    run()


