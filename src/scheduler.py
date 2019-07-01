'''
Created on Jul 26, 2018

@author: lorenzo
'''

import sys
import datetime
from itertools import cycle


def build_scheduler(config):
    s_type = config.get("scheduler", "type")
    if s_type == "periodic":
        return PeriodicScheduler(config)
    elif s_type == "fixed":
        return FixedScheduler(config)
    else:
        raise ValueError("Invalid scheduler type")

    
def compute_delta(next_time):
    return datetime.datetime.now() - datetime.datetime.combine(datetime.date.today(), next_time)


class Scheduler(object):

    def __init__(self, config):
        self.sleeping_time = config.getint("general", "sleeping_time")
        
    def is_feeding_time(self):
        delta = compute_delta(self.next)
        return delta.days == 0 and 0 < delta.seconds < 60


class PeriodicScheduler(Scheduler):

    def __init__(self, config):
        Scheduler.__init__(self, config)
        
        start_on = config.get("scheduler", "start_on")
        if start_on == "now":
            self.next = datetime.datetime.now().time()
        else: 
            hh, mm = [int(x) for x in start_on.split(":")]
            self.next = datetime.time(hour=hh, minute=mm)
        
        feed_every = config.get("scheduler", "feed_every")
        hh, mm = [int(x) for x in feed_every.split(":")]
        self.feed_every = datetime.timedelta(hours=hh, minutes=mm)
        
    def set_next(self):
        self.next = (datetime.datetime.combine(datetime.date.today(), self.next) + self.feed_every).time()
        print("%s: next time: %s" % (datetime.datetime.now(), str(self.next)), file=sys.stderr)

        
class FixedScheduler(Scheduler):

    def __init__(self, config):
        Scheduler.__init__(self, config)
        
        times = []
        for t in config.get("scheduler", "times").split(","):
            hh, mm = [int(x) for x in t.split(":")]
            times.append(datetime.time(hh, mm))
            
        # function used to sort times according to the proximity from the current time
        def distance_from_now(t):
            delta = compute_delta(t)
            if delta.days < 0:
                return -delta.seconds
            else:
                return 86400 - delta.seconds
            
        sorted_times = sorted(times, key=distance_from_now)
        print("Sorted times: %s" % ", ".join([str(t) for t in sorted_times]), file=sys.stderr)
                    
        self.times = cycle(sorted_times)
        self.set_next()
        
    def set_next(self):
        self.next = next(self.times)
        print("%s: next time: %s" % (datetime.datetime.now(), str(self.next)), file=sys.stderr)
