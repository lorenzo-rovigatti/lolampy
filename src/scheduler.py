'''
Created on Jul 26, 2018

@author: lorenzo
'''

import sys
import datetime


class Scheduler(object):

    def __init__(self, config):
        start_on = config.get("scheduler", "start_on")
        if start_on == "now":
            self.next = datetime.datetime.now().time()
        else: 
            hour, minute = [int(x) for x in start_on.split(":")]
            self.next = datetime.time(hour=hour, minute=minute)
        
        feed_every = config.get("scheduler", "feed_every")
        hours, minutes = [int(x) for x in feed_every.split(":")]
        self.feed_every = datetime.timedelta(hours=hours, minutes=minutes)
        
    def is_feeding_time(self):
        delta = datetime.datetime.now() - datetime.datetime.combine(datetime.date.today(), self.next)
        return delta >= datetime.timedelta()

    def set_next(self):
        self.next = (datetime.datetime.combine(datetime.date.today(), self.next) + self.feed_every).time()
        print("Next time: %s" % str(self.next), file=sys.stderr)
        