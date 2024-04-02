import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "urls.settings")

import django
django.setup()

#from django.core.management import call_command

import json
from django.core.mail import send_mail
from authentication.models import Profile
from polls.models import Urlentry, Leads
import requests
import re
from datetime import datetime
from iptocc import get_country_code

#every 2 minutes urlentry updating robot, that invokes the get_country_code to urlentry records
# that have urlentry.location=="unrecognized"
# the RIR databases loading time is about 1 minute
# one location record update lasts around 0,5 second
# that's why 250 records in 2 minutes is set up

def setlocation(iptext):
    #invoke the slow get_country_code function
    iploc="not found"
    try:
        links = Leads.objects.filter(follower_fromwhere=iptext).order_by("-follow_date").get()
        if links[0].location != "unrecognized":
            iploc=links[0].location
        else:
            iploc = get_country_code(iptext)
    except:
        iploc=get_country_code(iptext)
    return iploc

def setlocation_lazy(iptext):
    #doesn't invoke the slow get_country_code function
    try:
        links = Leads.objects.filter(follower_fromwhere=iptext).order_by("-follow_date").get()
        if links[0].location!="unrecognized":
            iploc=links[0].location
    except:
        iploc = "not found"
    return iploc

def process_notifications():
    starting_datetime = datetime.now()
    counter = 0
    lines = []
    leadsrecordsall = Leads.objects.filter(location="unrecognized").order_by("follow_date")[:250]
    print("<<    " + str(leadsrecordsall.count()) + ' leads records found, starting processing at    >>'+str(starting_datetime))
    #leadsrecord = leadsrecordsall.get()
    for lead in leadsrecordsall:
        iptext = lead.follower_fromwhere
        iploc = setlocation(iptext)
        lead.location=iploc
        lead.save()
        print("<  record  "+str(counter) + ' processed at ' + str(datetime.now()))
        counter = counter+1

# The notify.txt file is expected to contain one JSON object per line, where each JSON object represents a notification. Each notification should have a user_id and a message. Here’s an example of how the notify.txt file might look:
#
# JSON
#
# {"user_id": 1, "message": "Cron job is working every minute. This is a notification for uby with id=1",  "subject": "Test of cron job"}
# crontab command
# source /home/uby/virtualenv/website4/3.7/bin/activate && cd /home/uby/website4 && python notify.py > /tmp/notify.log 2>&1

def run():
    process_notifications()

if __name__ == '__main__':
    run()


