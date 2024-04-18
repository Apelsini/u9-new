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
        iploc="not found"
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

def setlocation_hard(iptext):
    #invoke the slow get_country_code function but doesn't copy by similar records
    iploc="not found"
    try:
        iploc = get_country_code(iptext)
    except:
        iploc="not found"
    return iploc

def process_notifications():
    starting_datetime = datetime.now()
    counter = 0
    lines = []
    leadsrecordsall_count = Leads.objects.filter(location="unrecognized").order_by("follow_date").count()
    leadsrecordsall = Leads.objects.filter(location="unrecognized").order_by("follow_date")[:250]
    leadsno = leadsrecordsall.count()
    print("<<    " + str(leadsrecordsall.count()) + ' leads records found, starting processing at    >>'+str(starting_datetime))
    #leadsrecord = leadsrecordsall.get()
    for lead in leadsrecordsall:
        iptext = lead.follower_fromwhere
        iploc = setlocation(iptext)
        lead.location=iploc
        lead.save()
        print("<  record  "+str(counter) + ' processed at ' + str(datetime.now()))
        counter = counter+1
    #processing records with "not found" once again
    leadsrec = Leads.objects.filter(location="not found").order_by("follow_date")[:250]
    nfcounter = 0
    for lea in leadsrec:
        iptext = lea.follower_fromwhere
        iploc = setlocation_hard(iptext)
        lea.location=iploc
        lea.save()
        print("<  'not found' record  "+str(nfcounter) + ' processed one more time at ' + str(datetime.now()))
        nfcounter = nfcounter+1
    #writing the stats to file
    with open('locationsrobot.txt', 'r') as file:
        existinglines = file.readlines()[1:50]
        existinglines.append("\nRecords with unrecognized locations: "+str(leadsrecordsall_count)+". Out of it "+str(leadsno)+" processed from "+str(starting_datetime)+" to "+str(datetime.now())+" not recognised locations double checked for "+str(nfcounter)+" records")
        file.close()
    with open('locationsrobot.txt', 'w') as file:
        print(existinglines)
        file.writelines(existinglines)
        file.close()

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


