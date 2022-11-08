import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import math
enc_str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ23456789"
#print(len(enc_str))
reserved = len(enc_str) ** 3  # 3-symbols address space - from 0 to 12 960 000 - is reserved for registered users only.
max_capacity = len(enc_str) ** 5  # maximal address - 5 symbols
#in 4 symbols we can save 12960000 days or 35506.849315068495 years
#in 5 symbols we can save 777600000 links daily
#unregistered users address space from  12960000 to 777600000


# Create your models here.
class Urlentry(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    create_date = models.DateTimeField('date created', auto_now=True)
    url_text = models.TextField()
    url_id = models.BigIntegerField()
    url_short = models.CharField(max_length=7)
    snapshot = models.TextField()
    qr_code = models.TextField()
    datetime_available_from = models.DateTimeField('url available from', auto_now=False)
    datetime_available_to = models.DateTimeField('url available to', auto_now=False)
    partner_ads = models.TextField()
    def __str__(self):
        return self.url_short
    def num_to_sym_unregistered(intnum2):
        # converts numbers to 4-5-symbols string
        # only registered users can create shortened links with 4 symbols like u9.by/aBcD others - only 5 symbols length
        # intnum=intnum+reserved
        out_str = ''
        intnum=intnum2+reserved
        if (intnum > reserved) and (intnum < max_capacity):
            while intnum > len(enc_str) - 1:
                current = intnum % (len(enc_str) - 1)
                # print ('division=',current,enc_str[current])
                out_str = out_str + enc_str[current]
                intnum = math.floor(intnum / (len(enc_str) - 1))
                # print('rest=', intnum)
                # print('last=',enc_str[59])
            out_str = out_str + enc_str[intnum]
        else:
            out_str = ''
        return out_str
    def num_to_sym_registered(intnum):
        # converts numbers to 3-symbols string
        # only registered users can create shortened links with 4 symbols like u9.by/aBcD others - only 5 symbols length
        # intnum=intnum+reserved
        out_str = ''
        if 0 <= intnum <= reserved:
            while intnum > len(enc_str) - 1:
                current = intnum % (len(enc_str) - 1)
                # print ('division=',current,enc_str[current])
                out_str = out_str + enc_str[current]
                intnum = math.floor(intnum / (len(enc_str) - 1))
                # print('rest=', intnum)
                # print('last=',enc_str[59])
            out_str = out_str + enc_str[intnum]
        else:
            out_str = ''
        return out_str
    def sym_to_num(str_num):
        # makes reversed operation - converts string to number
        intnum = 0
        str_num = str_num[::-1]
        # print(str_num)
        for i in range(len(str_num)):
            if enc_str.find(str_num[i]) >= 0:
                if i == 0:
                    rest = enc_str.find(str_num[i])
                if 0 < i < len(str_num):
                    rest = rest * 60 + enc_str.find(str_num[i])
                #  print('symbol no=',i,' is', str_num[i],' its position ',enc_str.find(str_num[i]),'  result is ',rest)
        return rest

class Leads(models.Model):
    urlentry = models.ForeignKey(Urlentry, on_delete=models.CASCADE)
    follow_date = models.DateTimeField('date when link was followed', auto_now=True)
    follower_info = models.TextField()
    follower_os_info = models.TextField()
    follower_fromwhere = models.TextField()
    def __str__(self):
        return self.follower_info



